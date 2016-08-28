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

# if __name__ == '__main__':

db = SqliteDatabase()

def grouper(iterable, n, fillvalue=None):
  args = [iter(iterable)] * n
  return (filter(None, values) for values
          in izip_longest(fillvalue=fillvalue, *args))


song = None

config = get_config()

seconds = 6
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
result = set()
# channels
Fs = fingerprint.DEFAULT_FS
data = reader.get_recorded_data()
channel_amount = len(data)
matches = []

def find_matches(samples, Fs=fingerprint.DEFAULT_FS):
  hashes = fingerprint.fingerprint(samples, Fs=Fs)
  return return_matches(hashes)

# return_matches()
def return_matches(hashes):
  mapper = {}
  for hash, offset in hashes:
    mapper[hash.upper()] = offset
  values = mapper.keys()

  for split_values in grouper(values, 1000):
    print('in grouper')
    query = "SELECT upper(hash), song_fk, offset FROM fingerprints WHERE upper(hash) IN (%s);"
    query = query % ', '.join('?' * len(split_values));
    # print('query', query)

    x = db.executeAll(query, split_values)
    print('query-x', len(x))

    for hash, sid, offset in x:
      # (sid, db_offset - song_sampled_offset)
      yield (sid, offset - mapper[hash])

for channeln, channel in enumerate(data):
  # TODO: Remove prints or change them into optional logging.
  print("Fingerprinting channel %d/%d" % (channeln + 1, channel_amount))
  matches.extend(find_matches(channel))
  print("Finished channel %d/%d" % (channeln + 1, channel_amount))
  # result |= set(hashes)
# for hash, offset in hashes:
#   print(str(hash.upper()) + " " + str(offset))

# # result |= set([("62DE23A0CC87079C3BB9",999)])
# # print('result', result)
# mapper = {}
# for hash, offset in result:
#   mapper[hash.upper()] = offset
# values = mapper.keys()

# print(len(values))
# matches = []
# # set()

# matches.extend((sid, offset - mapper[hash],))

# for split_values in grouper(values, 1000):
#   print('in grouper')
#   query = "SELECT upper(hash), song_fk, offset FROM fingerprints WHERE upper(hash) IN (%s);"
#   query = query % ', '.join('?' * len(split_values));
#   # UNHEX
#   # print('query', query)

#   x = db.executeAll(query, split_values)
#   print('query-x', len(x))

#   for hash, sid, offset in x:
#     # (sid, db_offset - song_sampled_offset)
#     # x = (sid, offset - mapper[hash])
#     matches.extend((sid, offset - mapper[hash],))
#     # matches |= set([x])

print('matches', len(matches))
# sys.exit(0)

# print('end grouper', len(matches))
# print('matches', matches)

def align_matches(matches):
  diff_counter = {}
  largest = 0
  largest_count = 0
  song_id = -1
  for tup in matches:
    sid, diff = tup
    if diff not in diff_counter:
      diff_counter[diff] = {}
    if sid not in diff_counter[diff]:
      diff_counter[diff][sid] = 0
    diff_counter[diff][sid] += 1

    if diff_counter[diff][sid] > largest_count:
      largest = diff
      largest_count = diff_counter[diff][sid]
      song_id = sid

  # return song_id

  # extract idenfication
  # song = self.db.get_song_by_id(song_id)

  songM = db.get_song_by_id(song_id)

  # return match info
  nseconds = round(float(largest) / fingerprint.DEFAULT_FS *
                   fingerprint.DEFAULT_WINDOW_SIZE *
                   fingerprint.DEFAULT_OVERLAP_RATIO, 5)
  return {
      "SONG_ID" : song_id,
      "SONG_NAME" : songM[1],
      "CONFIDENCE" : largest_count,
      "OFFSET" : int(largest),
      "OFFSET_SECS" : nseconds,
      # Database.FIELD_FILE_SHA1 : song.get(Database.FIELD_FILE_SHA1, None),
  }

x = align_matches(matches)
print(x)
# y = db.get_song_by_id(x)
# print(y)
print(x['SONG_NAME'])
