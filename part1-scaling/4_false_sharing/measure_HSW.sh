#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 ./program #threads"
	exit
fi

perf stat --pfm-events=UNHALTED_CORE_CYCLES,RESOURCE_STALLS:RS,LONGEST_LAT_CACHE:REFERENCE,LONGEST_LAT_CACHE:MISS $1 $2
