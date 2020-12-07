import sys
[sys.path.append(i) for i in ['.', '..']]

from libs.comms.server import Server
from libs.comms.server_manager import ServerManager
from libs.comms.client import Client
from signal import signal, SIGINT
from terminal_api import Terminal_Handler
from time import sleep
from threading import Thread
#import sys

#port_number = 0

def shutdown(signal, frame):
    print('Shutting down terminal server...')
    ServerManager.get_instance().shutdown()
    exit(0)

#def query_transactions(client: Client, api: Terminal_Handler):
#    sleep(90)
#    client.send(api.send_all_transactions())

if __name__ == "__main__":

    port_number = 12458
    server_number = 12456
    if len(sys.argv) > 1:
        port_number = int(sys.argv[1]) 
    if len(sys.argv) > 2:
        server_number = int(sys.argv[2]) 

    terminal_handler = Terminal_Handler("terminal")

    tap_listener = Server(port=port_number)
    tap_listener.rx_callback = terminal_handler.on_tap

    server_manager = ServerManager.get_instance()
    server_manager.add_server(tap_listener)

    server_manager.run()

    client = Client(port=server_number)  #change port when we decide which ports to run each server at
    client.rx_callback = terminal_handler.send_all_transactions
    client.start()

    #client_proc = Thread(target=query_transactions, args=(client, terminal_handler,))
    #client_proc.start()

    signal(SIGINT, shutdown)
