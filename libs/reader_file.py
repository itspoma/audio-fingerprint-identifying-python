from reader import BaseReader
import os
from pydub import AudioSegment
from pydub.utils import audioop
import numpy as np
from hashlib import sha1

class FileReader(BaseReader):
  def __init__(self, filename):
    # super(FileReader, self).__init__(a)
    self.filename = filename

  """
  Reads any file supported by pydub (ffmpeg) and returns the data contained
  within. If file reading fails due to input being a 24-bit wav file,
  wavio is used as a backup.

  Can be optionally limited to a certain amount of seconds from the start
  of the file by specifying the `limit` parameter. This is the amount of
  seconds from the start of the file.

  returns: (channels, samplerate)
  """
  # pydub does not support 24-bit wav files, use wavio when this occurs
  def parse_audio(self):
    limit = None
    # limit = 10

    songname, extension = os.path.splitext(os.path.basename(self.filename))

    try:
      audiofile = AudioSegment.from_file(self.filename)

      if limit:
        audiofile = audiofile[:limit * 1000]

      data = np.fromstring(audiofile._data, np.int16)

      channels = []
      for chn in xrange(audiofile.channels):
        channels.append(data[chn::audiofile.channels])

      fs = audiofile.frame_rate
    except audioop.error:
      print('audioop.error')
      pass
        # fs, _, audiofile = wavio.readwav(filename)

        # if limit:
        #     audiofile = audiofile[:limit * 1000]

        # audiofile = audiofile.T
        # audiofile = audiofile.astype(np.int16)

        # channels = []
        # for chn in audiofile:
        #     channels.append(chn)

    return {
      "songname": songname,
      "extension": extension,
      "channels": channels,
      "Fs": audiofile.frame_rate,
      "file_hash": self.parse_file_hash()
    }

  def parse_file_hash(self, blocksize=2**20):
    """ Small function to generate a hash to uniquely generate
    a file. Inspired by MD5 version here:
    http://stackoverflow.com/a/1131255/712997

    Works with large files.
    """
    s = sha1()

    with open(self.filename , "rb") as f:
      while True:
        buf = f.read(blocksize)
        if not buf: break
        s.update(buf)

    return s.hexdigest().upper()
