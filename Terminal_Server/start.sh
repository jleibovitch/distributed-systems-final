if [ $# -eq 0 ]
  then
    echo "Usage: ./start.sh <port number (between 10000 and 30000)"
    exit 1
fi

export TERMINAL_PORT=$1

python3 main.py