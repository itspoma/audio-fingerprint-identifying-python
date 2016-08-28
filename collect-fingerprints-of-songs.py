#!/usr/bin/python
import os
import libs
import sys
from itertools import izip_longest

from libs.reader_file import FileReader
import libs.fingerprint as fingerprint

from libs.db_sqlite import SqliteDatabase

db = SqliteDatabase()

def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return (filter(None, values) for values
      in izip_longest(fillvalue=fillvalue, *args))

if __name__ == '__main__':
  path = "mp3/"
  for filename in os.listdir(path):
    if filename.endswith(".mp3"):
      reader = FileReader(path + filename)

      print(reader.parse_name())
      audio = reader.parse_audio()
      print(audio, audio['channels'])

      song_id = db.add_song(filename, audio['file_hash'])
      print('song_id', song_id)

      sys.exit(0)

      result = set()
      channel_amount = len(audio['channels'])

      for channeln, channel in enumerate(audio['channels']):
        print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
        hashes = fingerprint.fingerprint(channel, Fs=audio['Fs'])
        print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
        result |= set(hashes)

      values = []
      sid = 34
      for hash, offset in result:
        values.append((sid, hash, offset))

      for split_values in grouper(values, 1000):
        query = "INSERT INTO fingerprintsx (song_fk, hash, offset) VALUES (?, ?, ?)"
        print('split_values', len(split_values))
        cur.executemany(query, split_values)
        # c.execute()

      conn.commit()
      conn.close()

      sys.exit(0)

  # fingerprint all files in a directory
  print('aa')
