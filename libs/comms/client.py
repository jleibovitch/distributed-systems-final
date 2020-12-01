from socket import socket, SHUT_RDWR, AF_INET, SOCK_STREAM
from threading import Thread
from comms.message_handler import Message_Handler
from comms.message import Message

class Client:

    buffsize = 1 * 1024 # 1kb buffer

    def __init__(self, host_addr = "0.0.0.0", port = 12345, client_type: str, server_type: str):
        
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.host_addr = host_addr
        self.port = port
        self.readyToSend = False
        self.readyToRecieve = False
        self.data = None
        self.isConnected = False
        self.type = client_type
        self.senderID = {}
        self.senderID["type"] = type
        self.senderID["nodeID"] = -1
        self.recipientID = {}
        self.recipientID["type"] = server_type
        self.recipientID["nodeID"] = self.port

    def run(self):
        try:
            connection = Thread(target=self.open_connection, args=(self.socket,))
        except Exception as e:
            print(e)
            exit(1)

    def open_connection(self, socket):
        try:
            print("Connecting to server...")
            socket.connect((self.host_addr, self.port))
            self.socket.send(Message(self.senderID, self.recipientID, "", "register"))
            data = self.socket.recv(buffSize)
            data = Message.load_from_json(data.decode("UTF-8"))
            if (data.intent == "ack" and data.data = "success"):
                self.isConnected = True
                self.recipientID["nodeID"] = data.recipientID["nodeID"]
        except Exception as e:
            print(e)
            exit(1)

        while self.isConnected:
            while self.readyToRecieve:
                data = socket.recv(buffsize)
                data = Message.load_from_json(data.decode("UTF-8"))
                self.readyToRecieve = False

                if (data.intent == "pull" and data.senderID["type"] == "terminal"):
                    socket.send(self.data)

                    # TO-DO add more functionality
            
            while self.readyToSend:
                socket.send(Message(self.senderID, self.recipientID, self.data, "push"))
                self.readyToSend = False

    def send(self, data):
        if (not self.readyToSend):
            self.readyToSend = True
            self.data = data

    def recieve(self):
        self.readyToRecieve = True

    def shutdown(self):
        print("Shutting down client..")
        self.isConnected = False
        try:
            self.socket.shutdown(SHUT_RDWR)
            self.socket.close()
        except Exception as e:
            print(e)