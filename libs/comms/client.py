from socket import socket, SHUT_RDWR, AF_INET, SOCK_STREAM
from threading import Thread

class Client:

    buffsize = 1 * 1024 # 1kb buffer

    def __init__(self, host_addr = "0.0.0.0", port = 12345):
        
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.host_addr = host_addr
        self.port = port
        self.readyToSend = False
        self.data = None
        self.isConnected = False

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
            self.isConnected = True
        except Exception as e:
            print(e)
            exit(1)

        while self.isConnected:
            while self.readyToSend:
                socket.send(data)
                self.readyToSend = False
                data = socket.recv(buffsize)
                if data is not None:
                    info(data.decode("UTF-8"))

    def send(self, data):
        if (not self.readyToSend):
            self.readyToSend = True
            self.data = data

    def shutdown(self):
        print("Shutting down client..")
        self.isConnected = False
        try:
            self.socket.shutdown(SHUT_RDWR)
            self.socket.close()
        except Exception as e:
            print(e)