from server import Server
from signal import signal, SIGINT
from os import getenv

def shutdown(signal, frame):
    print('Shutting down...')
    server.shutdown()
    exit(0)

if __name__ == "__main__":
    server = Server("127.0.0.1", int(getenv("TERMINAL_PORT")))

    signal(SIGINT, shutdown)
    server.start()