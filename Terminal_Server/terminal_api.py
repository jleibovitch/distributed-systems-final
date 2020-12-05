from libs.comm.message import Message
from libs.models.node import Node
from db import Database

class Terminal_Handler:

    def __init__(self, node_type: str):
        self.node = Node(node_type)
        self.db = Database()

    def on_tap(self, data):
        data = Message.load_from_json(data)
        if data["key"] == "tap" and data["intent"] == "push":
            self.db.insert(data["data"])

    def send_all_transactions(self, data) -> dict:
        data = Message.load_from_json(data)
        if (data["key"] == "main" and data["intent"] == "pull":
            user_transactions = self.db.return_transactions()
            return Message(self.node.type, user_transactions, "push").to_json()
        return {}

    def close(self):
        db.close()
