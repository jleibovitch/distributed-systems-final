from os import getenv
from signal import signal, SIGINT

from main_server.db import Database
from main_server.server import Server
import main_server.message as message

def shutdown(sig, frame):
  print('Shutting down')

  if db is not None:
    db.shutdown()
    terminal_listener.shutdown()

  exit(0)

def on_rx(data: str):
    msg = message.load_from_json(data)
    print(msg)

if __name__ == '__main__':

  host = getenv("DB_HOST")
  user = getenv("DB_USER")
  password = getenv("DB_PASS")
  database = getenv("DB_NAME")

  db = Database(host, database, user, password)
  terminal_listener = Server() # li
  # web_listener = Server(port=12457)
  Server.rx_callback = on_rx 

  signal(SIGINT, shutdown)
  terminal_listener.run()
  # web_listener.run()
