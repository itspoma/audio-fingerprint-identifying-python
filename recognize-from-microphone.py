# import argparse
# from argparse import RawTextHelpFormatter
from libs.reader_microphone import MicrophoneReader
from libs.visualiser_console import VisualiserConsole as visual_peak
from libs.visualiser_plot import VisualiserPlot as visual_plot

# seconds = args.recognize[1]
seconds = 2
song = None

visualise_console = True
visualise_plot = True

reader = MicrophoneReader(None)

reader.start_recording(seconds = seconds)
print('started recording..')

bufferSize = int(reader.rate / reader.chunksize * seconds)

for i in range(0, bufferSize):
  nums = reader.process_recording()

  if visualise_console:
    print("%05d %s" % visual_peak.calc(nums))
  else:
    print('processing %d of %d..' % (i, bufferSize))

if visualise_plot:
  data = reader.get_recorded_date()[1]
  visual_plot.show(data)

reader.stop_recording()
print('recording has been stopped..')

# print('recorded %d ..' % (reader.get_recorded_time()))
# print('recorded %d ..' % (len(reader.data[0])))

# reader.save_recorded('test.wav')
