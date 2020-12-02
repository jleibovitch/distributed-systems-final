"""
Author: Jamieson Leibovitch
Api.py

The purpose of this file is to create a set of helper methods for utilizing the db
"""

from .db import Database
from libs.models.transaction import Transaction

from typing import List

def get_account_transactions(account_id: int, limit=0) -> List[Transaction]:
  
  values = [account_id]
  query = "select * from transactions where account_no = %s"

  if limit > 0:
    query += " limit %s"
    values.append(limit)

  query += " order by transaction_time"

  db = Database.get_instance()
  rows = db.query_dict(query, tuple(values))

  return list(map(lambda row: Transaction(row), rows))

def insert_transactions(transactions: List[Transaction]):
  
  transaction_query_strs = list(map(lambda _: "(%s, %s, %s, %s, %s)", transactions))

  transaction_values = list(map(lambda t: [t.transaction_id, t.account_no, t.location_no, t.transaction_time, t.transaction_value], transactions))

  values = [t for v in transaction_values for t in v]

  temp_transactions = "create temp table temp_transactions as with t (transaction_id, account_no, location_no, transaction_time, transaction_value) as (values "
  temp_transactions += ",".join(transaction_query_strs)
  temp_transactions += ") select * from t"

  db = Database.get_instance()
  db.modify(temp_transactions, args=values, commit=False) 
  count = db.modify("insert into transactions (select * from temp_transactions) on conflict do nothing")

  print("Added", count, "Transactions")
  if count > 0:

    update_balance_query = """
update account a
set balance = new_balance
from (
	select account_no, sum(transaction_value) as new_balance 
	from transactions
	join (
	  select distinct(account_no) from test
	) x
	using (account_no)
	group by account_no
) y
where a.account_no = y.account_no
"""
    update_count = db.modify(update_balance_query)
    print("Number of updated accounts:", update_count)

