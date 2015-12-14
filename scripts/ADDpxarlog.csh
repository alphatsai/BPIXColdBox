#!/bin/tcsh
if ( $1 == "" ) then
	echo "Please add the test directory" 
	echo "    ./ADDpxarlog.csh [dirctory]"
	echo "ex. ./ADDpxarlog.csh M3010_FullQualification_2015-07-27_09h56m_1437983808"
	exit
endif

set nowPath=$PWD
set testDir=$1
set nNoPxar=0

cd $testDir
	set fulltestDirs=`ls -l | grep Fulltest | awk '{print $9}'`
	foreach fulltestDir($fulltestDirs)
		cd $fulltestDir
		echo $fulltestDir"..."
		if ( ! ( -e pxar.log ) ) then
			echo ">> Created new pxar.log from commander_Fulltest.log"
			cp commander_Fulltest.log pxar.log
			@ nNoPxar++
		endif
		cd -
	end
	if ( $nNoPxar == 0 ) then
		echo ">> All fulltest directories have pxar.log!"
	endif
cd $nowPath
