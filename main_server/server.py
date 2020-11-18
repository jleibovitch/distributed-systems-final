"""
Server.py
"""

from socket import socket, SHUT_RDWR
from threading import Thread
from time import sleep

class Server:

    rx_callback = None
    running = True

    def __init__(self, ip="0.0.0.0", port=12456):

        self.socket = socket()
        self.socket.bind((ip, port))
        self.ip = ip
        self.port = port
    
    def run(self):

        self.socket.listen()
        print(f"Server listening on {self.ip}:{self.port}")
        
        while Server.running:
            client, _ = self.socket.accept()
            thread = Thread(target=self.handle_client, args=(client,))
            thread.start()



    def handle_client(self, client: socket):
        
        buffsize = 8 * 1024 # buffer up to 8kb

        requester = Thread(target=self.requester, args=(client,))
        requester.start()

        while Server.running:
            data = client.recv(buffsize)
            if data:
                if Server.rx_callback:
                    data = Server.rx_callback(data.decode("utf-8"))
                    client.send(data)


        client.close()


    def shutdown(self):
        print("Shutting down server")
        Server.running = False
        self.socket.shutdown(SHUT_RDWR)
        self.socket.close()


    def requester(self, client):

        while Server.running:
            sleep(60)
            client.send(b"request")

