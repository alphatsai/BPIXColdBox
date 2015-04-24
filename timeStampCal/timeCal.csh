#!/bin/tcsh
if ( $2 == '' ) then
	echo "Please input the file or calibration value"
	echo "		EX: ./timeCal.csh [file] [Cal Value:2082844798] "
	exit	
endif
set file=$1
set value=$2
set name=`echo $file | sed 's/\//_/g'| sed 's/\./_/g'`
set timeStamp=`cat $file | awk '{print $1}'`
set temperature=`cat $file | awk '{print $2}'`
set i=1
rm -f $name'_Cal.txt'
touch $name'_Cal.txt'
foreach timeS($timeStamp)
	set timeS_cal = `echo $timeS - $value | bc` 
	echo $timeS_cal $temperature[$i] >> $name'_Cal.txt'
	@ i++
end
