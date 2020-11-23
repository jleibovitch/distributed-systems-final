"""
Server.py
"""

from socket import socket, SHUT_RDWR
from threading import Thread
from time import sleep

class Server:

    running = True
    buffsize = 1 * 1024 # buffer up to 1kb

    def __init__(self, ip="0.0.0.0", port=12456):

        self.socket = socket()
        self.socket.bind((ip, port))
        self.ip = ip
        self.port = port
        self.clients = {}
        self.rx_callback = None

    def run(self):

        self.socket.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        
        while Server.running:
            client, _ = self.socket.accept()
            thread = Thread(target=self.handle_client, args=(client,))
            thread.start()

    def handle_client(self, client: socket):
        
        print("Client connected")
        rx = Thread(target=self.rx, args=(client,))
        rx.start()
        self.clients[client.getpeername()] = client

    def shutdown(self):
        print("Shutting down server")
        Server.running = False
        for (key, client) in self.clients.items():
            print("Closing", key)
            client.shutdown(SHUT_RDWR)
            client.close()
        
        self.socket.close()


    def rx(self, client):
        while Server.running:
            data = client.recv(Server.buffsize)
            if data:
                if Server.rx_callback:
                    data = self.rx_callback(data.decode("utf-8"))
                    client.send(data)

