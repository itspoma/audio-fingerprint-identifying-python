#!/usr/bin/python
import os
import libs
from libs.reader_file import FileReader
import libs.fingerprint as fingerprint
from libs.db_sqlite import SqliteDatabase

if __name__ == '__main__':
  db = SqliteDatabase()
  path = "mp3/"

  # fingerprint all files in a directory

  for filename in os.listdir(path):
    if filename.endswith(".mp3"):
      reader = FileReader(path + filename)
      audio = reader.parse_audio()

      song_id = db.add_song(filename, audio['file_hash'])

      print("%s - id=%s channels=%d" % (filename, song_id, len(audio['channels'])))

      hashes = set()
      channel_amount = len(audio['channels'])

      for channeln, channel in enumerate(audio['channels']):
        print(" fingerprinting channel %d/%d" % (channeln+1, channel_amount))

        channel_hashes = fingerprint.fingerprint(channel, Fs=audio['Fs'])
        channel_hashes = set(channel_hashes)

        print(" finished channel %d/%d, got %d hashes" % (channeln+1, channel_amount, len(channel_hashes)))

        hashes |= channel_hashes

      print(" finished fingerprinting, got %d unique hashes" % (len(hashes)))

      values = []
      for hash, offset in hashes:
        values.append((song_id, hash, offset))

      print(" storing %d hashes in db" % (len(values)))
      db.store_fingerprints(values)

  print('end')
