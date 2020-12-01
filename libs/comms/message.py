"""
Message.py 
Author: Jamieson Leibovitch
The purpose of this class is to define a message protocol for the system 
"""

from json import dumps, loads

class Message:

    def __init__(self, senderID: dict, recipientID: dict, data: dict, intent: str):
        self.data = data
        self.intent = intent
        self.senderID = senderID
        self.recipientID = recipientID

    def to_json(self) -> str:

        msg_dict = {
            "recipientID": self.recipientID,
            "senderID": self.senderID,
            "intent": self.intent,
            "data": self.data
        }

        return dumps(msg_dict)

    def to_str(self) -> str:
        return str(self)

    def __str__(self):
        return f"senderNodeID: {self.senderID['nodeID']}, senderType: {self.senderID['type']}, recipientNodeID: {self.recipientID['nodeID']}, recipientType: {self.recipientID['type']}, intent: {self.intent}, data: {self.data}"

    @staticmethod
    def load_from_json(json_msg) -> 'Message':
        msg = loads(json_msg)
        return Message(msg.get("senderID"), msg.get("recipientID"), msg.get("data"), msg.get("intent"))
