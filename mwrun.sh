#!/bin/bash

dcidemoaddr=dcidemo.media.mit.edu
latestarcurl='http://hubris.media.mit.edu:8080/job/lit-mw/job/memberweekdemo/lastSuccessfulBuild/artifact/build/_releasedir/*zip*/_releasedir.zip'
arcname=releases.zip

set -ex

# Do a bunch of fenagling to get things right.
mkdir extract
rm -rf ./*
pushd extract > /dev/null
wget $latestarcurl -O $arcname
unzip releases.zip
tar -xvzf lit-*-linux-arm.tar.gz
pushd $(ls -d lit-*/) > /dev/null
litpath=$(realpath lit)
popd > /dev/null
popd > /dev/null

pkpath=litdata/privkey.hex
if [ ! -e $pkpath ]; then
	mkdir -p $(dirname $pkpath)
	dd if=/dev/urandom bs=32 count=1 2> /dev/null | hexdump -e '32/1 "%02x" "\n"' > $pkpath
	cat $pkpath
fi

$litpath -v --unauthrpc \
	--dir=litdata \
	--tn3 0 \
	--reg $dcidemoaddr:18444 \
	--litereg $dcidemoaddr:19444 \
	--dusd $dcidemoaddr:26999 &

litpid=$!

LITVENDING_CONFIG=config.json ./vending.py
kill $litpid
