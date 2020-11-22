from sqlite3 import connect

class Database:
    DATA_LENGTH = 5
    def __init__(self):
        try:
            self.conn = connect('transactions.db')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS transactions (
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                TAP_NODE_ID INTEGER NOT NULL,
                ACCT_ID VARCHAR(36) NOT NULL,
                ORIG_BAL REAL NOT NULL,
                CHARGE REAL NOT NULL,
                TIMESTAMP VARCHAR(64) NOT NULL,
                TERMINAL_ID INTEGER NOT NULL
            )''')
        except Exception as e:
            print("Error while connecting to transactions db")

    def insert(self, data, terminal_id):
        if (data is None or len(data) != Database.DATA_LENGTH):
            print("Invalid data, transaction dropped...")
            return
        try:
            cursor = self.conn.execute("SELECT COUNT(ID) from TRANSACTIONS")
            index = cursor.fetchone()[0] + 1
            values = [index, data["Tap_Node_id"], data["Account_Number"], data["Original_Balance"], data["Trip_Charge"], data["Transaction_Timestamp"], terminal_id]
            self.conn.execute("INSERT INTO transactions(ID, TAP_NODE_ID, ACCT_ID, ORIG_BAL, CHARGE, TIMESTAMP, TERMINAL_ID) VALUES(?,?,?,?,?,?,?)", values)
            self.conn.commit()
            print("Transaction cached successfully")
        except Exception as e:
            print("Error while inserting transaction..is the db alive?")
                
    def return_transactions(self):
        try:
            cursor = self.conn.execute("SELECT ID, TAP_NODE_ID, ACCT_ID, ORIG_BAL, CHARGE, TIMESTAMP, TERMINAL_ID from TRANSACTIONS")
            transaction_data = list()
            for row in cursor:
                values = {}
                values["Transaction_id"] = row[0]
                values["Tap_Node_id"] = row[1]
                values["Account_Number"] = row[2]
                values["Original_Balance"] = row[3]
                values["Trip_Charge"] = row[4]
                values["Transaction_Timestamp"] = row[5]
                values["Location_id"] = row[6]
                transaction_data.append(values)
            return transaction_data
        except Exception as e:
            print("Error while connecting to transactions db..is the db alive?")

    def return_transactions_account(self, data):
        try:
            account_num = data["Account_Number"]
            cursor = self.conn.execute("SELECT ID, TAP_NODE_ID, ACCT_ID, ORIG_BAL, CHARGE, TIMESTAMP, TERMINAL_ID from TRANSACTIONS WHERE ACCT_ID=?", (account_num,))
            transaction_data = list()
            for row in cursor:
                values = {}
                values["Transaction_id"] = row[0]
                values["Tap_Node_id"] = row[1]
                values["Account_Number"] = row[2]
                values["Original_Balance"] = row[3]
                values["Trip_Charge"] = row[4]
                values["Transaction_Timestamp"] = row[5]
                values["Location_id"] = row[6]
                transaction_data.append(values)
            return transaction_data
        except Exception as e:
            print("Error while connecting to transactions db..is the db alive?")

    def close(self):
        self.conn.close()