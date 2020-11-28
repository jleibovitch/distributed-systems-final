from threading import Thread
from .server import Server

from typing import List

class ServerManager:

    instance = None

    def __init__(self):
        self.servers: List[Server] = []
        self.threads: List[Thread] = []

    @staticmethod
    def get_instance() -> 'ServerManager':
        if ServerManager.instance is None:
            ServerManager.instance = ServerManager()

        return ServerManager.instance

    def add_server(self, server: Server):
        self.servers.append(server)

    def run(self):
        
        for server in self.servers:
            worker = Thread(target=server.run)
            worker.start()
            self.threads.append(worker)

    def shutdown(self):
        print("Shutting down server manager")

        for server in self.servers:
            server.shutdown()

        for thread in self.threads:
            thread.join()
