from reader import BaseReader

class FileReader(BaseReader):
  def __init__(self, a):
    super(MicrophoneReader, self).__init__(a)

  def recognize(self, **b):
    print('test FileReader', b['seconds'])
