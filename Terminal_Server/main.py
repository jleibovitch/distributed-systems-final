from libs.comm.server import Server
from libs.comm.server_manager import ServerManager
from libs.comm.message import Message
from signal import signal, SIGINT
from db import Database
import sys

port_number = 12345 

def shutdown(signal, frame):
    print('Shutting down terminal server...')
    ServerManager.get_instance().shutdown()
    exit(0)

def on_tap(data, location=port_number) -> str:
    db = Database()
    data = Message.load_from_json(data)
    if (data["key"] == "Tap_Node" and data["intent"] == "Insert_Transaction")
    db.insert(data["data"], location)
    return None

def send_user_transactions(data) -> dict:
    db = Database()
    data = Message.load_from_json(data)
    if (data["key"] == "Web_Portal" and data["intent"] == "fetch")
    user_transactions = db.return_transactions_account(data["data"])
    return Message("Terminal_Server", user_transactions, "Return_Data").to_json()

def send_all_transactions(data) -> dict:
    db = Database()
    data = Message.load_from_json(data)
    if (data["key"] == "Main_Server" and data["intent"] == "fetch")
    user_transactions = db.return_transactions()
    return Message("Terminal_Server", user_transactions, "Return_Data").to_json()

if __name__ == "__main__":

    if (len(sys.arv) > 1):
        port_number = int(sys.argv[1])

    tap_listener = Server(port=port_number)
    web_listener = Server(port=port_number)
    main_listener = Server(port=port_number)

    tap_listener.rx_callback = on_tap
    web_listener.rx_callback = send_user_transactions
    main_listener.rx_callback = send_all_transactions

    server_manager = ServerManager.get_instance()
    server_manager.add_server(tap_listener)
    server_manager.add_server(web_listener)
    server_manager.add_server(main_listener)

    server_manager.run()

    signal(SIGINT, shutdown)
    