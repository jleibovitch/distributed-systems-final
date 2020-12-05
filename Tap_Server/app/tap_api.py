import sys
[sys.path.append(i) for i in ['.', '..']]

from libs.comm.message import Message
from libs.models.node import Node
from libs.models.transactions import Transaction

class Tap_Handler:

    terminal_location = 0

    def __init__(self, node_type: str):
        self.node = Node(node_type)
        self.data = None
        self.transaction = None

    def package_request(self, acct_no: int, route_charge: float) -> 'Message':
        transaction = Transaction(account_no=acct_no, location_no=terminal_location, transaction_time=datetime.utcnow(), transaction_value=route_charge)
        message = Message(self.node.type, transaction.to_json(), "push")
        return message
        