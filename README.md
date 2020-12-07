# Distributed Systems Final Project

## Group Members

| Name                | Student ID |
| ------------------- | ---------- |
| Jamieson Leibovitch | 100612845  |
| Darren Chan         | 100618756  |
| Umar Qureshi        | 100591742  |
| Umar Eshan          | 100634240  |

## Project Dependencies

* Our project requires a few dependencies that are listed in the Pipfile. 
* If you do not have pipenv on your machine, you can install the dependencies manually using pip
* Our project utilizes Python3.8, but any version of python 3 that is greater than 3.6 should work

* The list of dependencies below:
```
psycopg2
python-dotenv
bcrypt
email-validator
Flask
Flask-WTF
Flask-Bootstrap
Flask-Bcrypt
Flask-Login
Flask-SQLAlchemy
SQLAlchemy
WTForms
Pillow
```

## How To Run

1. Start the main server. From the root folder run the following command `./main_server/start.sh`
  * This will start the main server
  * The default ports are 12456 for the terminal servers, and 12457 for the web server
2. Start the terminal server. From its directory (Terminal_Server) run the shell script command: `./start.sh <port number> <main server port>`
 * For example: `./start.sh 10000` will start it on 10000 and listen at the default port
3. Start a tap server. From its directory (Tap_Server) run the following shell script command: `./start.sh <flask server port> <terminal port>`
  * As an example, `./start.sh 5001 10000` will start the tap server on port 5001 and connect it to the terminal server on port 10000
  * It is important to change this, as the web server listens on port 5000
4. Start the web server. In its directory, run `python run.py`
  * It will create a new database cache
  * It will connect to the main server

## How to test

* Go to port 5000 on your localhost, register a new user and visit their funds page
* Select the "add user funds", and add funds for your user
* You should be able to see the transaction propogate to the main server on the next period
* In the tap server, copy and paste the user account number from the add funds page (or the message)
  * Create a transaction, and you should see that a new transaction is made
* Reload the page after the update propogates, (log in if it logs you out), you should see that the transaction was made successfully
