from socket import socket, SHUT_RDWR, AF_INET, SOCK_STREAM
from threading import Thread
from queue import Queue

class Client:

    buffsize = 8 * 1024 # buffer up to 1kb

    def __init__(self, host_addr = "127.0.0.1", port = 0):
        self.socket = socket(AF_INET,SOCK_STREAM)
        self.host_addr = host_addr
        self.host_port = port
        self.isConnected = False
        self.rx_callback = None
        self.msg_queue = Queue()

    def start(self):
        try:
            print("Connecting to server...")
            self.socket.connect((self.host_addr, self.host_port))
            rx_thread = Thread(target=self.server_connect, args=(self.socket,))
            rx_thread.start()
        except Exception as e:
            print("Could not connect to the server.")

    def server_connect(self, socket: socket):
        print("Connected to server")
        self.isConnected = True
        rx = Thread(target=self.rx, args=(socket,))
        rx.start()
        tx = Thread(target=self.tx, args=(socket,))
        tx.start()

    def rx(self, socket: socket):
        while self.isConnected:
            data = socket.recv(Client.buffsize)
            if data:
                if self.rx_callback:
                    data = self.rx_callback(data.decode("utf-8"))
                    if data is not None:
                       self.msg_queue.put(data)

    def tx(self, socket: socket):
        while self.isConnected:
            while not self.msg_queue.empty():
                data = self.msg_queue.get()
                print(data)
                socket.send(data.encode("utf-8"))
                
    def send(self, data):
        self.msg_queue.put(data)

    def shutdown(self):
        print("Shutting down client..")
        self.isConnected = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()
