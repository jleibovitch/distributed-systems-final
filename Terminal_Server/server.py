from socket import socket, SHUT_RDWR
from threading import Thread
from db import Database
import json

class Server:
    running = True

    def __init__(self, host_addr = "127.0.0.1", port = 12345):
        self.socket = socket()
        self.socket.bind((host_addr, port))
        self.host_addr = host_addr
        self.port = port
        self.connections = list()
    
    def start(self):
        self.socket.listen()
        print("Terminal server is listening on {}:{}".format(self.host_addr, self.port))
        while Server.running:
            client, addr = self.socket.accept()
            thread = Thread(target = self.handle_client, args = (client,))
            thread.start()
            self.connections.append(thread)

    def handle_client(self, client):
        db = Database()
        while Server.running:
            data = client.recv(1024)
            if data:
                data = dict(json.loads(data.decode("UTF-8")))
                exec = Server.server_funcs.get(data["Identity"], lambda: bad_identity)
                exec(self, db, data, self.port)
                    
        client.close()
        db.close()

    def shutdown(self):
        print("Shutting down terminal server...")
        Server.running = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
        for connection in self.connections:
            connection.join()

    def insert_transaction(self, db, data, location):
        db.insert(data["Payload"], location)

    def fetch_transactions(self, db, data, location):
        return json.dumps(db.return_transactions())

    def fetch_user_transactions(self, db, data, location):
        return json.dumps(db.return_transactions_account(data["Payload"]))

    def bad_identity(self, db, data, location):
        print("Unknown connection")

    server_funcs = {
        "Tap_Node": insert_transaction,
        "Main_Server": fetch_transactions,
        "Web_Portal": fetch_user_transactions
    }
