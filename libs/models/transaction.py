"""
Transaction.py
Author: Jamieson Leibovitch

The purpose of this class is to represent a data model for the transaction table
"""

from datetime import datetime
from json import dumps
from uuid import uuid1

class Transaction:

  def __init__(self, transaction_dict: dict):
    self.transaction_id: uuid1 = transaction_dict.get("transaction_id", str(uuid1()))
    self.account_no: int = transaction_dict.get("account_no", -1)
    self.location_no: int = transaction_dict.get("location_no", -1)
    self.transaction_time: datetime = transaction_dict.get("transaction_time")
    self.transaction_value: float = transaction_dict.get("transaction_value", None)


  def to_json(self) -> dict:

    return {
      "transaction_id": self.transaction_id,
      "account_no": self.account_no,
      "location_no": self.location_no,
      "transaction_time": str(self.transaction_time),
      "transaction_value": self.transaction_value
    }

  def __str__(self):
    return dumps(self.to_json())
