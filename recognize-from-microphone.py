import matplotlib
matplotlib.use('TkAgg')

import sys

# import argparse
# from argparse import RawTextHelpFormatter

# import numpy
# import scipy
# import struct
# import pyaudio
# import threading
# import pylab

from libs.reader_microphone import MicrophoneReader
from libs.visualiser_console import VisualiserConsole as visual_peak
from libs.visualiser_plot import VisualiserPlot as visual_plot
import libs.fingerprint as fingerprint
from libs.config import get_config
from libs.db_mongo import MongoDatabase

config = get_config()
print(config)
# db = MongoDatabase()
# x = db.insert("test", {"aaaaaa":"cccc"})
# print(x)

sys.exit(0)

song = None

seconds = 1
chunksize = 2**12
channels = int(config['channels']) # 1=mono, 2=stereo

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
filename = "mic"
# for d in data:
for channeln, channel in enumerate(data):
  # TODO: Remove prints or change them into optional logging.
  print("Fingerprinting channel %d/%d for %s" % (channeln + 1,
                                                       channel_amount,
                                                       filename))
  # samples = d
  hashes = fingerprint.fingerprint(channel, Fs=Fs)
  print("Finished channel %d/%d for %s" % (channeln + 1, channel_amount,
                                                 filename))
  result |= set(hashes)

  # matches.extend(self.dejavu.find_matches(d, Fs=self.Fs))

for hash, offset in result:
  print(str(hash.upper()) + " " + str(offset))

