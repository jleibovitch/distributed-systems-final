"""
account.py
Author: Jamieson Leibovitch

The purpose of this class is to provide a data structure for an account
"""
from .transaction import Transaction

from json import dumps
from typing import List

class Account:

    def __init__(self, account_json: dict, transactions: List[Transaction] =[], cards: List[int] =[]):
        
        self.account_no = account_json.get("account_no", -1)
        self.first_name = account_json.get("first_name", "")
        self.last_name = account_json.get("last_name", "")
        self.phone_number = account_json.get("phone_number", "")
        self.email = account_json.get("email", "")
        self.balance = account_json.get("balance", None)
        self.transactions = transactions
        self.cards = cards


    def to_json(self) -> dict:
        return {
            "account_no": self.account_no,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "balance": self.balance,
            "transactions": list(map(lambda t: t.to_json(), self.transactions)),
            "cards": self.cards
        }

    def __str__(self):
        return dumps(self.to_json())
