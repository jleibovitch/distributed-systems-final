#!/bin/bash

#if [ $# -lt 2 ]
#  then
#    echo "Usage: ./start.sh <server port number (between 10000 and 30000) <node starting port number (between 5000 and 7000)> <number of nodes (optional)"
#    exit 1
#fi

#num_servers=0
#tap_port=$2

#if [[ "$3" && -z "${1//[0-9]}" ]]
#then
#    num_servers=$3
#else
#    num_servers=1
#fi

#for ((count=0; count<$num_servers;count++))
#do
#    echo "Starting location tap terminal at http://localhost:$tap_port..."
#    python3 run.py $tap_port > log_$tap_port 2>&1 &
#    tap_port=$((tap_port+1))
#done

python3 run.py $1
