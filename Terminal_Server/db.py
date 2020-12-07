"""
db.py
Author: Darren Chan

The purpose of this class is to provide local sqlite3 database handling
"""

from sqlite3 import connect
from libs.models.transaction import Transaction

class Database:
    def __init__(self):
        try:
            self.conn = connect('transactions.db')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                transaction_id VARCHAR(255) PRIMARY KEY NOT NULL,
                account_no INTEGER NOT NULL,
                location_no INTEGER NOT NULL,
                transaction_time VARCHAR(64) NOT NULL,
                transaction_value REAL NOT NULL
            )''')

        except Exception as e:
            print("Error while connecting to transactions db")

    def insert(self, transaction):
        if transaction is None:
            print("No data supplied, transaction dropped...")
            return
        try:
            values = [transaction["transaction_id"], transaction["account_no"], transaction["location_no"], transaction["transaction_time"], transaction["transaction_value"]]
            self.conn.execute("INSERT INTO transactions(transaction_id, account_no, location_no, transaction_time, transaction_value) VALUES(?,?,?,?,?)", values)
            self.conn.commit()
            print("Transaction cached successfully")
        except Exception as e:
            print(e)
                
    def return_transactions(self) -> list:
        try:
            cursor = self.conn.execute("SELECT transaction_id, account_no, location_no, transaction_time, transaction_value from TRANSACTIONS")
            transaction_data = list()
            for row in cursor:
                print(row)
                transaction = Transaction({ "transaction_id": row[0], "account_no": row[1], "location_no": row[2], "transaction_time": row[3], "transaction_value": row[4] })
                transaction_data.append(transaction)
            return transaction_data
        except Exception as e:
            print(e)
            return None

    def close(self):
        self.conn.close()
