#!/bin/bash

dcidemoaddr=dcidemo.media.mit.edu

set -ex

if [ ! -e lit ]; then
	git clone \
		--single-branch \
		-b memberweekdemo \
		--depth=1 \
		https://github.com/gertjaap/lit.git
fi

pushd lit > /dev/null
make lit lit-af
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
