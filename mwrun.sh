#!/bin/bash

dcidemoaddr=dcidemo.media.mit.edu
latestarcurl='http://hubris.media.mit.edu:8080/job/lit-mw/job/memberweekdemo/lastSuccessfulBuild/artifact/build/_releasedir/*zip*/_releasedir.zip'
arcname=releases.zip
venddelay=5

set -ex

# Do a bunch of fenagling to get things right.
mkdir -p extract
pushd extract > /dev/null
rm -rf ./*
wget -O $arcname $latestarcurl # this complains about wildcards, not a lot I can do about that
unzip releases.zip
arc=$(find . -name 'lit-*-linux-arm.tar.gz')
tar -xvzf $arc
pushd $(ls -d lit-*/) > /dev/null
litpath=$(realpath lit)
popd > /dev/null
popd > /dev/null

pkpath=litdata/privkey.hex
if [ ! -e $pkpath ]; then
	mkdir -p $(dirname $pkpath)
	dd if=/dev/urandom bs=32 count=1 2> /dev/null | hexdump -e '32/1 "%02x" "\n"' > $pkpath
	cat $pkpath
	echo '{}' > litdata/rates.json
fi

# If something fails we don't want to totally fail everything anymore.
set +e

$litpath -v --unauthrpc \
	--dir=litdata \
	--tn3 0 \
	--reg $dcidemoaddr:18444 \
	--litereg $dcidemoaddr:19444 \
	--dusd $dcidemoaddr:26999 &

litpid=$!

sleep $venddelay # need this because it takes lit some time to startup
LITVENDING_CONFIG=config.json ./vending.py
kill $litpid
