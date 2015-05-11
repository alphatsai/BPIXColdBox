#!/bin/tcsh
if ( $1 == 'help' ) then
	echo '[INFO] ./genTemperature.csh [output] [delayTime] '
	exit
endif

if  ( $1 == '' ) then
	set output='temperature.log'
else
	set output=$1
endif

if  ( $2 == '' ) then
	set sleepTime=4
else
	set sleepTime=$2
endif

if ( ! ( -e ../logfiles ) ) then
	mkdir -p ../logfiles
endif

if ( -e ../logfiles/$output ) then
	rm -f ../logfiles/$output
endif

touch ../logfiles/$output
echo ">> [INFO] Writing temperatue to ../logfiles/$output..."
set angle=0
set maxTemp=20
while (1)
	set timestemp = `date +"%s"` 
	set temperature = `./tempCosine.py $maxTemp $angle`
	echo "$timestemp $temperature" 
	echo "$timestemp $temperature" >> ../logfiles/$output
	@ angle++
	sleep $sleepTime
end
