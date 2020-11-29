from os import getenv
from signal import signal, SIGINT

from main_server.db import Database
from libs.comms.server import Server
from libs.comms.server_manager import ServerManager
from libs.comms.message import Message

def shutdown(sig, frame):
  print('Shutting down')

  # shutdown the manager
  ServerManager.get_instance().shutdown()

  if db is not None:
    db.shutdown()


def on_rx(data: str):
    msg = Message.load_from_json(data)
    print(str(msg))

if __name__ == '__main__':

  host = getenv("DB_HOST")
  user = getenv("DB_USER")
  password = getenv("DB_PASS")
  database = getenv("DB_NAME")

  db = Database(host, database, user, password)

  terminal_listener = Server() 
  web_listener = Server(port=12457)

  terminal_listener.rx_callback = on_rx 

  server_manager = ServerManager.get_instance()
  server_manager.add_server(terminal_listener)
  server_manager.add_server(web_listener)

  server_manager.run()

  signal(SIGINT, shutdown)

  
  # terminal_listener.run()
  # web_listener.run()
