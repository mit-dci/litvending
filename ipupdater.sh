#!/bin/bash

sleeptime=$1
hostaddr=$2
destfile=$3

while true; do
	ip=$(ip a show dev wlp1s0 | grep 'inet ' | sed 's/\// /g' | awk '{ print $2 }')
	echo $ip | ssh $hostaddr bash -c "cat - > $destfile"
	sleep $sleeptime
done
