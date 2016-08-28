from db import Database
from config import get_config
import sqlite3
import sys

class SqliteDatabase(Database):
  def __init__(self):
    pass

  def connect(self):
    config = get_config()

    self.conn = sqlite3.connect('db/fingerprints.db')
    self.cur = self.conn.cursor()

  def select(self, table, params):
    self.connect()

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
    self.connect()

    keys = ', '.join(params.keys())
    values = params.values()

    query = "INSERT INTO songs (%s) VALUES (?, ?)" % (keys);

    self.cur.execute(query, values)
    self.conn.commit()

    return self.cur.lastrowid


