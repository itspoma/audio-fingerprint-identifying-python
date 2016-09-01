#!/usr/bin/python
import sys, os
sys.path.append(os.path.join(sys.path[0], '..'))

from libs.db_sqlite import SqliteDatabase
from termcolor import colored

if __name__ == '__main__':
  db = SqliteDatabase()

  row = db.executeOne("SELECT 2+3 as x;")

  assert row[0] == 5, "failed simple sql execution"
  print ' * %s' % colored('ok', 'green')
