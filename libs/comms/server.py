"""
Server.py
"""

from socket import socket, SHUT_RDWR
from threading import Thread
from time import sleep

class Server:

    buffsize = 1 * 1024 # buffer up to 1kb

    def __init__(self, ip="0.0.0.0", port=12456):

        self.socket = socket()
        self.socket.bind((ip, port))
        self.ip = ip
        self.port = port
        self.clients = {}
        self.rx_callback = None
        # self.rx_thread: Thread = None
        self.running = True

    def run(self):

        self.socket.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        
        try:
            while self.running:
                client, _ = self.socket.accept()
                rx_thread = Thread(target=self.handle_client, args=(client,))
                rx_thread.start()
        except OSError:
            print("Server Socket Closed")

    def handle_client(self, client: socket):
        
        print("Client connected")
        rx = Thread(target=self.rx, args=(client,))
        rx.start()
        self.clients[client.getpeername()] = client

    def shutdown(self):
        self.running = False
        print(f"Shutting down server on {self.ip}:{self.port}")
        for (key, client) in self.clients.items():
            print("Closing", key)
            client.shutdown(SHUT_RDWR)
            client.close()

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

