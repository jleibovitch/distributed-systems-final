"""
web_api.py
Author: Umar Ehsan

The purpose of this class is to provide a handler service for message handling (incoming and outgoing)
"""

import sys
[sys.path.append(i) for i in ['.', '..']]

from server.models import db, User, Cards
from libs.comms.message import Message
from libs.models.node import Node
from libs.models.transaction import Transaction
from libs.models.account import Account
from .models import Transactions

from typing import List

class Web_Handler:

    def __init__(self, node_type: str, db: db):
        self.node = Node(node_type)
        self.db = db

    def push_account(self, acct_no: int) -> str:
        """
        Register that a new account is created
        """
        print("Registering new account:", acct_no)
        return str(Message(self.node.type, {"account_no": acct_no}, "push_account"))

    def request_transactions(self, acct_no: int) -> str:
        data = {}
        data["account_no"] = acct_no
        message = Message(self.node.type, data, "pull_transactions")
        return str(message)

    def handle_incoming(self, data):
        print("Recieved", data)
        data = Message.load_from_json_str(data)

        if data.key == "main":
            # main server pushes transactions
            if data.intent == "push_transactions":
                if len(data.data["transactions"]) == 0:
                    print("No transactions found for user", data.data["account_no"])
                else:
                    self.store_user_transactions(list(map(lambda t: Transaction(t), data.data["transactions"])))
            elif data.intent == "pull_transactions":
                # TODO: get all cached transactions

                transactions = Transactions.query.all()
                transactions_list = list()

                for t in transactions:
                    msg_Addfunds = {
                                  "transaction_id": t.transaction_id,
                                  "account_no": t.account_no,
                                  "location_no": t.location_no,
                                  "transaction_time": str(t.transaction_time),
                                  "transaction_value": t.transaction_value
                                }

                    transactions_list.append(msg_Addfunds)

                return str(Message("web", transactions_list, "push_transactions"))

    def store_user_transactions(self, transactions: List[Transaction]):

            user = User.query.filter_by(account_no=transactions[0].account_no).first()
            if user:
                card = Cards.query.filter_by(user_id=user.id).first()
                if card:
                    funds = 0
                    for transaction in transactions:
                        funds += transaction.transaction_value

                    card.funds = funds
                    db.session.commit()
                    print('User balance updated')
        
