import sys

class Database(object):
  def __init__(self, a):
    self.a = a

  def connect(self): pass
  def insert(self, table, params): pass

  def add_song(self, filename, filehash):
    song = self.findOne('songs', {
      "filehash": filehash
    })

    if not song:
      song_id = self.insert('songs', {
        "name": filename,
        "filehash": filehash
      })
    else:
      song_id = song[0]

    return song_id
