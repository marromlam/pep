#!/bin/bash

if [ $# -ne 2 ]
then
	echo "Usage: $0 ./program #threads"
	exit
fi

perf stat --pfm-events=UNHALTED_CORE_CYCLES,RESOURCE_STALLS:MEM_RS,LAST_LEVEL_CACHE_REFERENCES,LAST_LEVEL_CACHE_MISSES $1 $2
