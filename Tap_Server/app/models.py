from uuid import uuid1
from random import randint

class Transaction():
    def __init__(self):
        self.account_num = uuid1()
        self.starting_balance = randint(100, 200)