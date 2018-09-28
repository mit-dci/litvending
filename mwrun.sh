#!/bin/bash

dcidemoaddr=dcidemo.media.mit.edu
latestarcurl='http://hubris.media.mit.edu:8080/job/lit-mw/job/memberweekdemo/lastSuccessfulBuild/artifact/build/_releasedir/lit-161aa3d-linux-arm.tar.gz'
arcname=build.tar.gz

set -ex

wget $latestarcurl -O $arcname
tar -xvzf $arcname
pushd $(ls -d lit-*/) > /dev/null
litpath=$(realpath lit)
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
