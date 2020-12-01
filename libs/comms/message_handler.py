"""
Message Handler
"""
from socket import socket, SHUT_RDWR
from threading import Thread
from time import sleep
from comms import Message
from Terminal_Server.db import Database

bufferSize = 1 * 1024   # 1kb buffer

class Message_Handler:
    def __init__(self, senderID: int, senderType: str, localEndPoint: socket, remoteEndPoint: socket):
        self.senderID = {}
        self.senderID["nodeID"] = senderID
        self.senderID["type"] = senderType
        self.localEndPoint = localEndPoint
        self.conns = {}
        self.isRunning = True
        self.remoteEndPoint = remoteEndPoint
    
    def set_remote_end_point(self, conn: socket):
        self.remoteEndPoint = conn

    def run(self):
        if (self.senderID["type"] == "terminal"):
            tap_thread = Thread(target=self.handle_taps, args=(conns,))
            tap_thread.start()
            if (self.remoteEndPoint is not None):
                # start a main client thread instead of client.run?

        if (self.senderID["type"] == "main"):
            terminal_thread = Thread(target=self.handle_terminals, args=(conns,))
            web_thread = Thread(target=self.handle_portals, args=(conns,))
            terminal_thread.start()
            web_thread.start()

    def register(self, conn: socket):
        try:
            data, addr = conn.recv(bufferSize)
            data = Message.load_from_json(data.decode("UTF-8"))
            if (data.intent == "register"):
                self.conns[conn.getpeername()] = {}
                self.conns[conn.getpeername()]["recipientID"]["type"] = data.recipientID["type"]
                self.conns[conn.getpeername()]["recipientID"]["nodeID"] = addr
                self.conns[conn.getpeername()]["client"] = conn
                conn.send(Message(self.senderID, self.conns[conn.getpeername()]["recipientID"], "success", "ack"))
            print("Client successfully registered")
            return True
        except:
            print("Error registering client, closing...")
            exit(1)
        return False

    def handle_taps(self, clients: dict):
        while self.isRunning:
            for (key, client) in self.clients.items():
                try:
                    if (client["recipientID"]["type"] == "tap"):
                        cliend.send(Message(self.senderID, client["recipientID"], "", "pull"))
                        data = client.recv(bufferSize)
                        data = Message.load_from_json(data.decode("UTF-8"))
                        if (data.recipientID["nodeID"] == client["recipientID"]["nodeID"] and data.intent == "push" and data.data is not None):
                            db = Database()
                            self.on_tap(db, data.data, self.senderID["nodeID"])
                except:
                    print("Error while sending request for tap data")
            sleep(5)

    def handle_terminals(self, clients: dict):
        while self.isRunning:
            for (key, client) in self.clients.items():
                try:
                    if (client["recipientID"]["type"] == "terminal"):
                        cliend.send(Message(self.senderID, client["recipientID"], "", "pull"))
                        data = client.recv(bufferSize)
                        data = Message.load_from_json(data.decode("UTF-8"))
                        if (data.recipientID["nodeID"] == client["recipientID"]["nodeID"] and data.intent == "push" and data.data is not None):
                            # use the main server's db operation here
                except:
                    print("Error while sending request for tap data")
            sleep(120)

    def handle_portals(self, clients: dict):
        while self.isRunning:
            for (key, client) in self.clients.items():
                try:
                    if (client["recipientID"]["type"] == "web"):
                        cliend.send(Message(self.senderID, client["recipientID"], "", "push"))
                        data = client.recv(bufferSize)
                        data = Message.load_from_json(data.decode("UTF-8"))
                        if (data.recipientID["nodeID"] == client["recipientID"]["nodeID"] and data.intent == "pull" and data.data == "ready"):
                            db = Database()
                            client.send(Message(self.senderID, client["recipientID"], db.send_all_transactions, "push"))
                except:
                    print("Error while sending request for tap data")
            sleep(120)

    def on_tap(self, db, data, location=port_number):
        data = Message.load_from_json(data)
        if (data["key"] == "Tap_Node" and data["intent"] == "Insert_Transaction")
        db.insert(data["data"], location)

    def send_user_transactions(self, db, data) -> dict:
        data = Message.load_from_json(data)
        if (data["key"] == "Web_Portal" and data["intent"] == "fetch")
        user_transactions = db.return_transactions_account(data["data"])
        return user_transactions

    def send_all_transactions(self, db, data) -> dict:
        data = Message.load_from_json(data)
        if (data["key"] == "Main_Server" and data["intent"] == "fetch")
        user_transactions = db.return_transactions()
        return user_transactions

    def shutdown(self):
        self.isRunning = False