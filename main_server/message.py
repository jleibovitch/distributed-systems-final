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

    def to_json(self) -> str:

        msg_dict = {
            "key": self.key,
            "intent": self.intent,
            "data": self.data
        }

        return dumps(msg_dict)

def load_from_json(json_msg) -> Message:
    msg = loads(json_msg)
    return Message(msg.get("key"), msg.get("data"), msg.get("intent"))
