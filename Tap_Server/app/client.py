from socket import socket, SHUT_RDWR, AF_INET, SOCK_STREAM
from threading import Thread
from logging import warning, info
from time import sleep

class Client:
    def __init__(self, host_addr = "127.0.0.1", port = 12345):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.host_addr = host_addr
        self.port = port
        self.isConnected = False

    def start(self):
        try:
            warning("Connecting to server...")
            self.socket.connect((self.host_addr, self.port))
            self.isConnected = True
        except Exception as e:
            warning(e)


    def send(self, data):
        if (self.isConnected):
            self.socket.send(data)

    def shutdown(self):
        warning("Shutting down client..")
        self.isConnected = False
        try:
            self.socket.shutdown(SHUT_RDWR)
            self.socket.close()
        except Exception as e:
            warning(e)