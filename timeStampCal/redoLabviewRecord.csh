#!/bin/tcsh
if ( $2 == "" ) then
	echo "To bulid new file, saperate each pt1000"
	echo ""
	echo "./redoLabviewRecord.csh [labveiw_Log] [pt1000_Label]"
	echo ""
	echo "Ex:  ./redoLabviewRecord.csh T_history_2013-10-23.tsv 1"
	exit
endif

set log_=$1
set outputName=`echo $log_ | sed 's/\./_/g' | sed 's/\ /_/g'`
set w_=$2
if ( $w_ == 1 ) then
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$3}' >! "$outputName"_1
else if ( $w_ == 2 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$4}' >! "$outputName"_2
else if ( $w_ == 3 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$5}' >! "$outputName"_3
else if ( $w_ == 4 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$6}' >! "$outputName"_4
else if ( $w_ == 5 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$7}' >! "$outputName"_5
else if ( $w_ == 6 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$8}' >! "$outputName"_6
else if ( $w_ == 7 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$9}' >! "$outputName"_7
else if ( $w_ == 8 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$10}' >! "$outputName"_8
else if ( $w_ == 9 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$11}' >! "$outputName"_9
else if ( $w_ == 10 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$12}' >! "$outputName"_10
else if ( $w_ == 11 ) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$13}' >! "$outputName"_11
else if ( $w_ == 12) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$14}' >! "$outputName"_12
else if ( $w_ == 13) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$15}' >! "$outputName"_13
else if ( $w_ == 14) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$16}' >! "$outputName"_14
else if ( $w_ == 15) then	
	cat $log_ | grep -v 'Timestamp' | awk '{print $1" "$17}' >! "$outputName"_15
endif


