"""
main_server.py
Author: Jamieson Leibovitch

The purpose of this class is to initialize and manage the main server in our Distributed System. It communicates with the main db
"""

from os import getenv
from signal import signal, SIGINT
from threading import Thread
from time import sleep

from .db import Database
from libs.comms.server import Server
from libs.comms.server_manager import ServerManager
from libs.comms.message import Message
from .main_handler import Main_Handler

import main_server.api as api

db: Database = None

def shutdown(sig, frame):
  print('Shutting down')

  # shutdown the manager
  ServerManager.get_instance().shutdown()

  if db is not None:
    db.shutdown()

def request_terminal(client):
    message = Message("main", {}, "pull")
    client.send(str(message).encode('utf-8'))


def on_rx(data: str):
    msg = Message.load_from_json(data)
    print(str(msg))

def main():
  host = getenv("DB_HOST")
  user = getenv("DB_USER")
  password = getenv("DB_PASS")
  database = getenv("DB_NAME")

  db = Database(host, database, user, password)

  print(list(map(lambda t: str(t), api.get_account_transactions(10000000))))

  main_handler = Main_Handler("main")

  terminal_listener = Server(port=12456) 
  web_listener = Server(port=12457)

  terminal_listener.rx_callback = main_handler.insert_transactions
  terminal_listener.on_connected_callback = request_terminal

  web_listener.rx_callback = main_handler.send_transactions

  server_manager = ServerManager.get_instance()
  server_manager.add_server(terminal_listener)
  server_manager.add_server(web_listener)

  def round_robin():
      
      while terminal_listener.running:
          sleep(10)
          print("Requesting terminl data")
          for client in terminal_listener.clients.values():
              request_terminal(client)
              sleep(1) # allow 1 second between messages

  rr = Thread(target=round_robin)
  rr.daemon = True
  rr.start()

  server_manager.run()

  signal(SIGINT, shutdown)

