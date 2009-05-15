#!/bin/bash

# This script is to take the signed.zip file from the signing lab and perform 
#  the necessary steps to prepare the update.rdf and fix the zip file

CURDIR=$(pwd)
cd $(dirname $0)
SCRIPTDIR=$(pwd)

#------------------------------------------------------------------------------
function fail
{
	echo "Failed: $1"
	exit 1
}

#------------------------------------------------------------------------------
# The purpose of this is the recreate the zip with zigbert.rsa as
#  the first file in the zip. Firefox 3 requires this.
# https://developer.mozilla.org/en/Signing_a_XPI#Prepare_XPI_file_for_signing

function reorder_xpi
{
	rm -rf tmp
	unzip -d tmp $1
	cd tmp

	zip $1 META-INF/zigbert.rsa || fail "Missing zigbert.rsa"
	zip $1 META-INF/zigbert.sf || fail "Missing zigbert.sf"
	zip $1 META-INF/manifest.mf || fail "Missing manifest.mf"

	zip $1 chrome.manifest || fail "Missing chrome.manifest"
	zip $1 install.rdf || fail "Missing install.rdf"

	zip -r $1 plugins  || fail "Missing plugins"
	zip -r $1 skin || fail "Missing skin"

	cd ..

	mv $1 $1.orig
	mv tmp/$1 .

	rm -rf tmp
}

#------------------------------------------------------------------------------
# Check to make sure there are two xpis in the zip file
function check_zip
{
	XPIS=$(unzip -l $1 | grep xpi | awk '{print $4}')
	COUNT=$(echo $XPIS | wc -w)
	test x$COUNT == x2 || fail "Only $COUNT file in the zip file"
}

#------------------------------------------------------------------------------
# Pass in the rdf file to be signed
function sign_update_rdfs
{
	MCCOY=$HOME/Desktop/mccoy/mccoy
	#./mccoy -command install -installRDF $1 -key moonlight -xpi novell-moonlight-1.9.1-i586.xpi

	# Passing -xpi just generates and adds the sha1 hash to the file
	# The hash is is already generated in create_update_rdfs.py
	$MCCOY -command install -installRDF $SCRIPTDIR/$1 -key moonlight

}

#------------------------------------------------------------------------------
# MAIN function

test  $# -eq 1 || fail "Usage: $0 <moonlight_signed.zip>"
test  -e $1 || fail "Cannot find file $1"

# Delete any old generated files
rm -f novell*xpi* update*.rdf info*.xhtml

check_zip $1
unzip $1

for xpi in $XPIS
do
	echo "Reordering $xpi"
	reorder_xpi $xpi
done

VERSIONS=$(cat VERSIONS)  #read versions from file
NEW_VERSION=$(echo $VERSIONS | awk '{print $NF}')  # set new version to the last version in the list
OLD_VERSIONS=$(echo $VERSIONS | sed -e "s#$NEW_VERSION##") # remove the last version from the list
OLD_VERSIONS=$(echo $OLD_VERSIONS | sed -e 's#\ #,#g') # change list to a comma separated list

./create_update_rdfs.py -p 2.0 -a i586,x86_64 -n $NEW_VERSION -o $OLD_VERSIONS

for rdf in $(ls update*.rdf)
do
	sign_update_rdfs $rdf
done
#!/bin/bash


# upload all necessary files to go-mono
#scp novell-moonlight*xpi info*xhtml mono-web@go-mono.com:go-mono/archive/moonlight-plugins/$NEW_VERSION
#scp update-2.0*rdf mono-web@go-mono.com:go-mono/archive/moonlight-plugins/updates
