from os import getenv
from signal import signal, SIGINT
from db import Database
from server import Server


def shutdown(sig, frame):
  print('Shutting down')

  if db is not None:
    db.shutdown()

  exit(0)


if __name__ == '__main__':

  host = getenv("DB_HOST")
  user = getenv("DB_USER")
  password = getenv("DB_PASS")
  database = getenv("DB_NAME")

  db = Database(host, database, user, password)
  server = Server()

  signal(SIGINT, shutdown)
  server.run()
