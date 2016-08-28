import sys

class Database(object):
  TABLE_SONGS = None
  TABLE_FINGERPRINTS = None

  def __init__(self, a):
    self.a = a

  def connect(self): pass
  def insert(self, table, params): pass

  def add_song(self, filename, filehash):
    song = self.findOne(self.TABLE_SONGS, {
      "filehash": filehash
    })

    if not song:
      song_id = self.insert(self.TABLE_SONGS, {
        "name": filename,
        "filehash": filehash
      })
    else:
      song_id = song[0]

    return song_id

  def store_fingerprints(self, values):
    self.insertMany(self.TABLE_FINGERPRINTS,
      ['song_fk', 'hash', 'offset'], values
    )
