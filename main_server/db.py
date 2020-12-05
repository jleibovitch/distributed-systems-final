"""
db.py

This is a db wrapper class to provide some assistance in querying the database
"""
import psycopg2 as pq
from psycopg2.extras import DictCursor

class Database:

  instance = None

  def __init__(self, host, db, user, password):

    try:
      self.db_connection = pq.connect(host=host, user=user, password=password, database=db)
    except pq.DatabaseError as e:
      print(e)
      exit(1)

    Database.instance = self

  def query_dict(self, query, args=None):

    with self.db_connection.cursor(cursor_factory=DictCursor) as cursor:
      cursor.execute(query, args)
      rows = cursor.fetchall()

    return rows

  def modify(self, query, args=None, commit=True) -> int:
    with self.db_connection.cursor() as cursor:

      cursor.execute(query, args)
      if commit:
        self.db_connection.commit()
      count = cursor.rowcount

    return count

  def shutdown(self):
    self.db_connection.close()


  @staticmethod
  def get_instance() -> 'Database':

    if Database.instance is None:
      print("ERROR: Database is not initialized")
      # TODO: Change to proper shutdown
      exit(1)

    return Database.instance
