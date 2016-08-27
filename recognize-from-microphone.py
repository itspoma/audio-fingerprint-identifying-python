print('recognize-from-microphone.py');

class BaseRecognizer(object):
  def __init__(self, a):
    self.a = a

  def _recognize(self, *data):

