#!/usr/bin/python
from libs.db_sqlite import SqliteDatabase

if __name__ == '__main__':
  db = SqliteDatabase()

  row = db.executeOne("""
    SELECT
      (SELECT COUNT(*) FROM songs) as songs_count,
      (SELECT COUNT(*) FROM fingerprints) as fingerprints_count
  """)

  print('songs - %d' % row[0]);
  print('fingerprints - %d' % row[1]);

  print('done');
