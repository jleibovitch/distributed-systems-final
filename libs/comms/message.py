"""
Message.py 
Author: Jamieson Leibovitch
The purpose of this class is to define a message protocol for the system 
"""

from json import dumps, loads

class Message:

    def __init__(self, key: str, data: dict, intent: str):
        self.key = key
        self.data = data
        self.intent = intent

    def to_json(self) -> dict:

        msg_dict = {
            "key": self.key,
            "intent": self.intent,
            "data": self.data
        }
        
        return msg_dict

    def to_str(self) -> str:
        return str(self)

    def __str__(self):
        return dumps(self.to_json())

    @staticmethod
    def load_from_json_str(json_msg: str) -> 'Message':
        msg = loads(json_msg)
        return Message.load_from_json(msg)

    @staticmethod
    def load_from_json(msg: dict) -> 'Message':
        return Message(msg.get("key"), msg.get("data"), msg.get("intent"))
