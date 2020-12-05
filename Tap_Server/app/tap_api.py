import sys
[sys.path.append(i) for i in ['.', '..']]

from libs.comms.message import Message
from libs.models.node import Node
from libs.models.transaction import Transaction
from datetime import datetime
from uuid import uuid1

class Tap_Handler:

    terminal_location = 0

    def __init__(self, node_type: str):
        self.node = Node(node_type)
        self.data = None
        self.transaction = None

    def package_request(self, acct_no: int, terminal_location: int, route_charge: float) -> str:
        transaction = Transaction({ "transaction_id": str(uuid1()), "account_no": acct_no, "location_no": terminal_location, "transaction_time": datetime.utcnow(), "transaction_value": route_charge })
        message = Message(self.node.type, transaction.to_json(), "push")
        return str(message.to_str())
        