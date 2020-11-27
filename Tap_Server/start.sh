#!/bin/bash

if [ $# -eq 0 ]
  then
    echo "Usage: ./start.sh <port number (between 10000 and 30000) <number of nodes (optional)>"
    exit 1
fi

export TERMINAL_PORT=$1

num_servers=0
tap_port=5000

if [[ "$2" && -z "${1//[0-9]}" ]]
then
    num_servers=$2
else
    num_servers=1
fi

for ((count=0; count<$num_servers;count++))
do
    echo "Starting location tap terminal at http://localhost:$tap_port..."
    flask run -p $tap_port > log_$tap_port 2>&1 &
    tap_port=$((tap_port+1))
done