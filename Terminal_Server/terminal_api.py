from libs.comms.message import Message
from libs.models.node import Node
from db import Database

class Terminal_Handler:

    def __init__(self, node_type: str):
        self.node = Node(node_type)

    def on_tap(self, data):
        db = Database()
        data = Message.load_from_json_str(data).to_json()
        if data["key"] == "tap" and data["intent"] == "push":
            db.insert(data["data"])

    def send_all_transactions(self, data) -> dict:
        data = Message.load_from_json_str(data).to_json()
        db = Database()
        if data["key"] == "main" and data["intent"] == "pull":
            user_transactions = db.return_transactions()
            return Message(self.node.type, user_transactions, "push").to_json()
        return {}

    def close(self):
        db.close()
