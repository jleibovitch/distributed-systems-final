import sys
[sys.path.append(i) for i in ['.', '..']]

from .models import db, User, Cards
from libs.comms.message import Message
from libs.models.node import Node
from libs.models.transaction import Transaction
from libs.models.account import Account

class Web_Handler:

    def __init__(self, node_type: str, db: db):
        self.node = Node(node_type)
        self.db = db

    def package_request(self, acct_no: int) -> 'Message':
        data = {}
        data["account_no"] = acct_no
        message = Message(self.node.type, data, "pull")
        return message

    def store_user_transactions(self, data):
        data = Message.load_from_json(data)
        if data["key"] == "main" and data["intent"] == "push":
            account = Account(data["data"]["account"], data["data"]["transactions"])
            user = User.query.filter_by(account_no=data).first()
            if user:
                card = Cards.query.filter_by(user_id=user.id).first()
                if card:
                    for transaction in account.transactions:
                        card.funds += transaction.transaction_value
                    db.session.commit()
                    print('User balance updated')
        
