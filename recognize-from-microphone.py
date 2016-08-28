#!/usr/bin/python

import libs
import sys

from libs.reader_microphone import MicrophoneReader
from libs.visualiser_console import VisualiserConsole as visual_peak
from libs.visualiser_plot import VisualiserPlot as visual_plot
import libs.fingerprint as fingerprint
from libs.config import get_config
from itertools import izip_longest
from libs.db_sqlite import SqliteDatabase
# from libs.db_mongo import MongoDatabase

db = SqliteDatabase()

def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return (filter(None, values) for values
          in izip_longest(fillvalue=fillvalue, *args))


song = None

config = get_config()

seconds = 5
chunksize = 2**12
channels = 2#int(config['channels']) # 1=mono, 2=stereo

record_forever = False
visualise_console = bool(config['mic.visualise_console'])
visualise_plot = bool(config['mic.visualise_plot'])

reader = MicrophoneReader(None)

reader.start_recording(seconds=seconds,
  chunksize=chunksize,
  channels=channels)
print('started recording..')

while True:
  bufferSize = int(reader.rate / reader.chunksize * seconds)

  for i in range(0, bufferSize):
    nums = reader.process_recording()

    if visualise_console:
      print("%05d %s" % visual_peak.calc(nums))
    else:
      print('processing %d of %d..' % (i, bufferSize))

  if not record_forever: break

if visualise_plot:
  data = reader.get_recorded_data()[0]
  visual_plot.show(data)

reader.stop_recording()
print('recording has been stopped..')

# print('recorded %d ..' % (reader.get_recorded_time()))
# print('recorded %d ..' % (len(reader.data[0])))

# reader.save_recorded('test.wav')

# DEFAULT_FS = 44100
# result = set()
# channels
Fs = fingerprint.DEFAULT_FS
data = reader.get_recorded_data()
channel_amount = len(data)

for channeln, channel in enumerate(data):
  # TODO: Remove prints or change them into optional logging.
  print("Fingerprinting channel %d/%d" % (channeln + 1, channel_amount))
  hashes = fingerprint.fingerprint(channel, Fs=Fs)
  print("Finished channel %d/%d" % (channeln + 1, channel_amount))

  # for hash, offset in hashes:
  #   print(str(hash.upper()) + " " + str(offset))

  mapper = {}
  for hash, offset in hashes:
    mapper[hash.upper()] = offset
  values = mapper.keys()

  # print(len(values))
  matches = []

  for split_values in grouper(values, 1000):
    print('in grouper')
    query = "SELECT hash, song_fk, offset FROM fingerprints WHERE hash IN (%s);"
    query = query % ', '.join('?' * len(split_values));
    # UNHEX
    print('query', query)

    x = db.executeAll(query, split_values)
    print('query-x', x)

    # for hash, sid, offset in db.cur:
      # (sid, db_offset - song_sampled_offset)
      # matches.extend((sid, offset - mapper[hash]))

  print('end grouper', len(matches))

  # result |= set(hashes)


# db = MongoDatabase()
# x = db.insert("test", {"aaaaaa":"cccc"})
# print(x)

# if __name__ == '__main__':

