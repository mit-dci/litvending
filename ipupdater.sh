#!/bin/bash

iface=$1
sleeptime=$2
hostaddr=$3
destfile=$4

while true; do
	ip=$(ip a show dev $iface | grep 'inet ' | sed 's/\// /g' | awk '{ print $2 }')
	echo $ip | ssh $hostaddr bash -c "cat - > $destfile"
	sleep $sleeptime
done
