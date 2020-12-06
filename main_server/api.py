"""
Author: Jamieson Leibovitch
Api.py

The purpose of this file is to create a set of helper methods for utilizing the db
"""

from .db import Database
from libs.models.transaction import Transaction
from libs.models.account import Account

from typing import List

def get_account_transactions(account_id: int, limit=0) -> List[Transaction]:
  """
  Get a list of transactions for an account,with an optional limit of transactions
  """
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
  """
  Insert a list of transactions into the database, and then update the user's balance
  """

  if len(transactions) == 0:
      return

  # Create a set of queries
  transaction_query_strs = list(map(lambda _: "(%s, %s, %s, %s, %s)", transactions))
  transaction_values = list(map(lambda t: [t.transaction_id, t.account_no, t.location_no, t.transaction_time, t.transaction_value], transactions))

  values = [t for v in transaction_values for t in v]

  temp_table = "create temp table temp_transactions(transaction_id uuid, account_no int, location_no int, transaction_time timestamp, transaction_value float)"
  # temp_transactions = "create temp table temp_transactions as with t (transaction_id, account_no, location_no, transaction_time, transaction_value) as (values "
  temp_transactions = "insert into temp_transactions values "
  temp_transactions += ",".join(transaction_query_strs)
  # temp_transactions += ")"

  db = Database.get_instance()
  db.modify("drop table if exists temp_transactions")
  db.modify(temp_table, args=values, commit=False) 
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
	  select distinct(account_no) from temp_transactions
	) x
	using (account_no)
	group by account_no
) y
where a.account_no = y.account_no
"""
    update_count = db.modify(update_balance_query)
    print("Number of updated accounts:", update_count)


def get_user_cards(account_id: int) -> List[int]:
    """
    Get a list of cards for a user
    """
    query = "select card_id from card where account_no = %s"
    db = Database.get_instance()
    rows = db.query_dict(query, (account_id,))

    return list(map(lambda c: c.get("card_id"), rows))

def register_user_card(account_id: int, card_id: int):

    query = "insert into card values (%s, %s)"

    db = Database.get_instance()
    count = db.modify(query, (card_id, account_id))

    assert count == 1

def get_user_account_info(account_id: int) -> Account:
  """
  Get the user account information for a specific id
  """

  query = "select * from account where account_no = %s"

  db = Database.get_instance()
  rows = db.query_dict(query, (account_id,))

  assert len(rows) == 1

  transactions = get_account_transactions(account_id)
  cards = get_user_cards(account_id)

  return Account(rows[0], transactions, cards)

def register_user_account(account_no: int):
    """
    Insert into the database a new account
    """

    query = "insert into account values (%s, %s) "#%s, %s, %s, %s)"
    values = (account_no, 0)

    db = Database.get_instance()
    count = db.modify(query, values)

    assert count == 1
