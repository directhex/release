#!/bin/sh

confdir=$(dirname $(pwd)/$0)
packagingdir=$confdir/../packaging
. $packagingdir/shared-code.sh



WEB_DIR=$1

cd $WEB_DIR

for distro_conf in $packagingdir/conf/*-*-*; do
	
	distro_info `basename $distro_conf`
	
	mkdir -p $DISTRO
	
	OUT=$DISTRO/index.html
	

	rm -rf $OUT
	
	cat $confdir/groups | while read line
	do
		if [ "x${line:0:1}" == "x#" ]; then
			ARGS=(${line:1})
			RPMS=()
			for package in ${ARGS[@]:1}; do 
				. $packagingdir/defs/$package
				
				ships_package || continue
				get_destroot
			
				[ -d $DEST_ROOT/$package/*/ ] || continue
						
				VERSION=`ls -d $DEST_ROOT/$package/*/ -t -1 | head -n1`
				
				for i in $VERSION/*.rpm; do
					[[ $i == *.src.rpm ]] && continue
					RPMS=(${RPMS[@]} $i)
				done
			done
			
			if [ ${#RPMS[@]} -eq 0 ]; then
				echo "<p>Not available for this platform</p>" >> $OUT
				continue
			fi
			
			zipname=${ARGS[0]}
			
			rm -rf $DISTRO/$zipname.zip
			zip -j $DISTRO/$zipname.zip ${RPMS[@]}
			
			echo "<p>All these files in a <a href='$zipname.zip'>.zip file</a></p>" >> $OUT
			echo "<ul>" >> $OUT
			
			for i in ${RPMS[@]}; do
				NAME=$(rpm -qp --queryformat '%{VERSION}' $one_rpm 2>/dev/null)
				echo "<ul><a href='../$i'>$NAME</a></ul>" >> $OUT
			done
			
			echo "</ul>" >> $OUT
			
		elif [ "x${line:0:1}" == "x!" ]; then
			line=$(echo ${line:1})
			
			. $confdir/$line >> $OUT
			
		else
			echo ${line//\\[\\[arch\\]\\]/$(basename $distro_conf)} >> $OUT
		fi
	done
done