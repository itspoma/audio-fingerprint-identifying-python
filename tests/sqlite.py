import sqlite3
conn = sqlite3.connect('db/fingerprints.db')
c = conn.cursor()

c.execute("INSERT INTO fingerprints (song_fk, hash) VALUES (11,'asd')")

conn.commit()
conn.close()
