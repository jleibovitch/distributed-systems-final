from sqlite3 import connect
from libs.models.transaction import Transaction

class Database:
    def __init__(self):
        try:
            self.conn = connect('transactions.db')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
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
            cursor = self.conn.execute("SELECT COUNT(transaction_id) from TRANSACTIONS")
            index = cursor.fetchone()[0] + 1
            values = [index, transaction["account_no"], transaction["location_no"], transaction["transaction_time"], transaction["transaction_value"]]
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
                transaction = Transaction(row[0], row[1], row[2], row[3], row[4])
                transaction_data.append(values)
            return transaction_data
        except Exception as e:
            print(e)
            return None

    def close(self):
        self.conn.close()