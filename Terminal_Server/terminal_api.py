from libs.comms.message import Message
from libs.models.node import Node
from db import Database

class Terminal_Handler:

    def __init__(self, node_type: str):
        self.node = Node(node_type)

    def on_tap(self, data):
        db = Database()
        data = Message.load_from_json_str(data)
        if data.key == "tap" and data.intent == "push":
            db.insert(data.data)

    def send_all_transactions(self, data) -> str:
        data = Message.load_from_json_str(data)
        db = Database()
        if data.key == "main" and data.intent == "pull":
            user_transactions = db.return_transactions()
            return str(Message(self.node.type, list(map(lambda t: t.to_json(), user_transactions)), "push"))
        return None

    def close(self):
        db.close()
