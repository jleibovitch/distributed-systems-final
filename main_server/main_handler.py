from libs.comms.message import Message
from libs.models.node import Node
from libs.models.transaction import Transaction
import main_server.api as api

class Main_Handler:

    def __init__(self, node_type: str):
        self.node = Node(node_type)

    def insert_transactions(self, data):
        print(data)
        data = Message.load_from_json_str(data)
        if data.key == "terminal" and data.intent == "push":
            api.insert_transactions(list(map(lambda t: Transaction(t), data.data)))

    def send_transactions(self, data) -> Message:
        data = Message.load_from_json_str(data)
        if data.key == "web" and data.intent == "pull":
            print(data.data)
            acct_no = data.data["account_no"]
            msg = Message(self.node.type, api.get_account_transactions(acct_no), "push")
            return str(msg)
        return None
