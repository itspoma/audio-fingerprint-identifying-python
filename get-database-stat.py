#!/usr/bin/python
from libs.db_sqlite import SqliteDatabase
from termcolor import colored

# get summary information
def printSummary():
  row = db.executeOne("""
    SELECT
      (SELECT COUNT(*) FROM songs) as songs_count,
      (SELECT COUNT(*) FROM fingerprints) as fingerprints_count
  """)

  msg = ' * %s: %s (%s)' % (
    colored('total', 'yellow'),             # total
    colored('%d song(s)', 'yellow'),        # songs
    colored('%d fingerprint(s)', 'yellow')  # fingerprints
  )
  print msg % row

  return row[0] # total

# get songs \w details
def printSongs():
  rows = db.executeAll("""
    SELECT
      s.id,
      s.name,
      (SELECT count(f.id) FROM fingerprints AS f WHERE f.song_fk = s.id) AS fingerprints_count
    FROM songs AS s
    ORDER BY fingerprints_count DESC
  """)

  for row in rows:
    msg = '   ** %s %s: %s' % (
      colored('id=%s','white',attrs=['dark']), # id
      colored('%s', 'white', attrs=['bold']),   # name
      colored('%d hashes', 'green')             # hashes
    )
    print msg % row

# find duplicates
def printDuplicates():
  rows = db.executeAll("""
    SELECT a.song_fk, s.name, SUM(a.cnt)
    FROM (
      SELECT song_fk, COUNT(*) cnt
      FROM fingerprints
      GROUP BY hash, song_fk, offset
      HAVING cnt > 1
      ORDER BY cnt ASC
    ) a
    JOIN songs s ON s.id = a.song_fk
    GROUP BY a.song_fk
  """)

  msg = ' * duplications: %s' % colored('%d song(s)', 'yellow')
  print msg % len(rows)

  for row in rows:
    msg = '   ** %s %s: %s' % (
      colored('id=%s','white',attrs=['dark']),
      colored('%s', 'white', attrs=['bold']),
      colored('%d duplicate(s)', 'red')
    )
    print msg % row

# find colissions
def printColissions():
  rows = db.executeAll("""
    SELECT sum(a.n) FROM (
      SELECT
        hash,
        count(distinct song_fk) AS n
      FROM fingerprints
      GROUP BY `hash`
      ORDER BY n DESC
    ) a
  """)

  msg = ' * colissions: %s' % colored('%d hash(es)', 'red')
  val = 0
  if rows[0][0] is not None:
    val = rows[0]

  print msg % val

if __name__ == '__main__':
  db = SqliteDatabase()
  print ''

  x = printSummary()
  printSongs()
  if x: print ''

  printDuplicates()
  if x: print ''

  printColissions()

  print '\ndone'
