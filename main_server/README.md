# Main Server

## To run

1. Use pipenv

2. Install the dependencies
  * Psycopog2
  * Might require the binary -> `pip3 install psycopg2-binary`

## To test

* In a separate terminal, run netcat, which is installed via package manager
  * Ex: `sudo apt install netcat`

* Run the following: `nc -v 127.0.0.1 12456 <<< '{"key": "test", "intent": "0", "data": "hello world"}'`
* You may run a similar command with different key, intent and data
