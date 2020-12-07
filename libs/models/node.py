"""
Node.py
Author: Umar Ehsan

The purpose of this class is to provide a data structure for node identification (server or client)
"""

from uuid import uuid1
from json import dumps

class Node:
    def __init__(self, type: str):
        self.type = type
        self.id = uuid1()

    def to_json(self) -> dict:
        return {
        "node_id": self.id,
        "node_type": self.type
        }

    def __str__(self):
        return dumps(self.to_json())