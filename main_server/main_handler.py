from libs.comms.message import Message
from libs.models.node import Node
from libs.models.account import Account
from libs.models.transaction import Transaction
import main_server.api as api

class Main_Handler:

    def __init__(self, node_type: str):
        self.node = Node(node_type)

    def insert_transactions(self, data):
        print(data)
        data = Message.load_from_json_str(data)
        if (data.key == "terminal" and data.intent == "push") or (data.key == "web" and data.intent == "push_transactions"):
            api.insert_transactions(list(map(lambda t: Transaction(t), data.data)))

    def handle_incoming_web_request(self, data):

        msg = Message.load_from_json_str(data)

        return_data = None

        if msg.key == "web":
            print("Recieved from web", str(msg))
            # register account
            if msg.intent == "push_account":
                api.register_user_account(msg.data["account_no"])
            elif msg.intent == "pull_transactions":
                return_data = self.send_transactions(msg.data)

        return return_data


    def send_transactions(self, data) -> str:
        acct_no = data["account_no"]
        transactions = api.get_account_transactions(acct_no)
        msg = Message(self.node.type, Account({"account_no": acct_no}, transactions=transactions).to_json(), "push_transactions")
        return str(msg).encode('utf-8')
