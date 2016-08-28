from db import Database
from config import get_config
import sqlite3
import sys
from itertools import izip_longest

class SqliteDatabase(Database):
  def __init__(self):
    self.connect()

  def connect(self):
    config = get_config()

    self.conn = sqlite3.connect('db/fingerprints.db')
    self.cur = self.conn.cursor()
    print('sqlite - connection opened')

  def __del__(self):
    self.conn.close()
    print('sqlite - connection has been closed')

  def query(self, query, values = []):
    self.cur.execute(query, values)

  def select(self, table, params):
    conditions = []
    values = []

    for k, v in enumerate(params):
      key = v
      value = params[v]
      conditions.append("%s = ?" % key)
      values.append(value)

    conditions = ' AND '.join(conditions)
    query = "SELECT * FROM %s WHERE %s" % (table, conditions)

    self.cur.execute(query, values)

  def findOne(self, table, params):
    self.select(table, params)
    return self.cur.fetchone()

  def findAll(self, table, params):
    self.select(table, params)
    return self.cur.fetchall()

  def insert(self, table, params):
    keys = ', '.join(params.keys())
    values = params.values()

    query = "INSERT INTO songs (%s) VALUES (?, ?)" % (keys);

    self.cur.execute(query, values)
    self.conn.commit()

    return self.cur.lastrowid

  def insertMany(self, table, columns, values):
    def grouper(iterable, n, fillvalue=None):
      args = [iter(iterable)] * n
      return (filter(None, values) for values
          in izip_longest(fillvalue=fillvalue, *args))

    for split_values in grouper(values, 1000):
      query = "INSERT OR IGNORE INTO %s (%s) VALUES (?, ?, ?)" % (table, ", ".join(columns))
      self.cur.executemany(query, split_values)

    self.conn.commit()
