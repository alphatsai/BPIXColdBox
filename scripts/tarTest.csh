#!/bin/tcsh
if ( $1 == "" ) then
	echo "Please add the test directory" 
	echo "    ./tarTest.csh [dirctory] (submit)"
	echo "ex. ./tarTest.csh M3010_FullQualification_2015-07-27_09h56m_1437983808 submit"
	exit
endif
if ( ! -e $1 ) then
	echo ">> ERROR: Not found $1"
	exit
endif
if ( -e $1.tar.gz ) then
	echo ">> ERROR: $1.tar.gz already exist!"
	exit
endif

set gzdir="gzFilesForDB"
set module=`echo $1 | sed 's/\///g'`
echo "tar $module to $gzdir/$module.tar.gz..."
tar -czf $gzdir/$module.tar.gz $module 

if ( $2 == 'submit' ) then
	cd $gzdir
	scp -P 23481 "$module.tar.gz" cern@cmspixelprod.pi.infn.it:/home/cern/dropbox
	scp "$module.tar.gz" pcpixeltb02:/home/pixel_dev/MoReWeb/DATA/tar/ThermalCycling
	cd -
endif
