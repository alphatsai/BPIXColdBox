#!/bin/tcsh

set tarDir='/home/pixel_dev/MoReWeb/DATA/tar/ThermalCycling'
if ( $1 == "" ) then
	echo '>> [INFO] Please input options'
	echo '>>        Input module name or "all"'
	echo '>>        ./xTar.csh M3024'
	echo '>>        ./xTar.csh all'
else if ( $1 == 'all' ) then
	set tars=`ls -l $tarDir | grep tar.gz | grep M30 | awk '{print $9}'`
	set numTest=`echo $tars | wc -w`
	echo ">> [INFO] $numTest tests will be submited to DB"
	echo ">>        http://cmspixelprod.pi.infn.it"
	echo ">> [INFO] Extracting tar.gz now..."
	foreach tar( $tars )
		echo ">>        $tar..."
		tar -xzf $tarDir/$tar
	end
else
	set tars=`ls -l $tarDir | grep tar.gz | grep $1 | awk '{print $9}'`
	set numTest=`echo $tars | wc -w`
	echo ">> [INFO] $numTest tar.gz in $tarDir"
	echo ">> [INFO] Extracting $1 now..."
	foreach tar( $tars )
		set name=`echo $tar | sed 's/\(.*\).tar.gz/\1/g'`
		if ( -e $name ) then
			echo ">>        [WARNING] $tar extracted before. Nothing to do!"
		else
			echo ">>        $tar..."
			tar -xzf $tarDir/$tar
		endif
	end
endif
