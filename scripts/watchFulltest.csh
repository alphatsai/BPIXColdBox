#!/bin/tcsh
if ( $1 == "" ) then
	echo "Please add the test directory" 
	echo "    ./watchFulltest.csh [dirctory] [line<1000]"
	echo "ex. ./watchFulltest.csh M3010_FullQualification_2015-07-27_09h56m_1437983808 50"
	exit
endif
if ( ! ( -e $1 ) ) then
	echo ">> [ERROR] $1 doesn't exist!"
	exit
endif
set line=$2
if ( $2 == "" || $2 > 1000 ) then
	set line=20
endif

set testDir = `ls -ltr $1 | tail -n1 | awk '{print $9}'`
set log = `ls -ltr $1/$testDir | grep log | grep commander | tail -n1 | awk '{print $9}'`
echo ">> [INFO] Watching $1/$testDir/$log"
watch tail -n$line $1/$testDir/$log
#echo $testDir
