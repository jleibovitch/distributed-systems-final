from libs.comm.server import Server
from libs.comm.server_manager import ServerManager
from libs.comm.client import Client
from signal import signal, SIGINT
from terminal_api import Terminal_Handler
from Thread import sleep
import sys

port_number = 0

def shutdown(signal, frame):
    print('Shutting down terminal server...')
    ServerManager.get_instance().shutdown()
    exit(0)

if __name__ == "__main__":

    if (len(sys.arv) > 1):
        port_number = int(sys.argv[1])

    terminal_handler = Terminal_Handler("terminal")

    tap_listener = Server(port=port_number)
    tap_listener.rx_callback = terminal_handler.on_tap

    server_manager = ServerManager.get_instance()
    server_manager.add_server(tap_listener)

    server_manager.run()

    client = Client(port=0)  #change port when we decide which ports to run each server at
    client.start()
    client_proc = Thread(target=send_transactions, args=(client, terminal_handler,))
    client_proc.start()

    signal(SIGINT, shutdown)
    
def query_transactions(client: Client, api: Terminal_Handler):
    Thread.sleep(90)
    client.send(api.send_all_transactions())