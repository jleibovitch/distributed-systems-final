"""
Server.py
"""

from socket import socket, SHUT_RDWR
from threading import Thread
from time import sleep
from comms import Message_Handler
from comms.client import Client

class Server:

    buffsize = 1 * 1024 # buffer up to 1kb

    def __init__(self, ip="0.0.0.0", port=12456, server_type, client_type = None):

        self.socket = socket()
        self.socket.bind((ip, port))
        self.ip = ip
        self.port = port
        self.clients = {}
        self.rx_callback = None
        # self.rx_thread: Thread = None
        self.running = True
        self.type = server_type
        self.clientType = client_type
        self.main = None
        self.message_handler = Message_Handler(self.port, self.type, self.socket, self.main)

    def run(self):

        self.socket.listen()
        print(f"Server listening on {self.ip}:{self.port}")

        cliendID = 
        self.main = Client("0.0.0.0", 15000, clientType, self.type) #pick the correct port for actual connection when testing
        self.message_handler.set_remote_end_point(self.main)
        self.message_handler.run()

        try:
            while self.running:
                client, _ = self.socket.accept()
                rx_thread = Thread(target=self.handle_client, args=(client,))
                rx_thread.start()
        except OSError:
            print("Server Socket Closed")

    def handle_client(self, client: socket):
        
        print("Connecting with client")
        if self.message_handler.register(client):
            self.clients[client.getpeername()] = client

    def shutdown(self):
        self.running = False
        print(f"Shutting down server on {self.ip}:{self.port}")
        for (key, client) in self.clients.items():
            print("Closing", key)
            client.shutdown(SHUT_RDWR)
            client.close()

        self.message_handler.shutdown()
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()


    def rx(self, client):
        while self.running:
            data = client.recv(Server.buffsize)
            if data:
                if self.rx_callback:
                    data = self.rx_callback(data.decode("utf-8"))
                    if data is not None:
                        client.send(data)

