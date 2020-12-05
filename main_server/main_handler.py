from libs.comms.message import Message
from libs.models.node import Node
import main_server.api as api

class Main_Handler:

    def __init__(self, node_type: str):
        self.node = Node(node_type)

    def insert_transactions(self, data):
        data = Message.load_from_json(data)
        if data["key"] == "terminal" and data["intent"] == "push":
            api.insert_transactions(data["data"])

    def send_transactions(self, data) -> 'Message':
        data = Message.load_from_json(data)
        if data["key"] == "web" and data["intent"] == "pull":
            acct_no = data["data"]["account_no"]
            msg = Message(self.node.type, api.get_account_transactions(acct_no), "push")
            return msg
        return None