import numpy as np

class VisualiserConsole():
  def __init__(self):
    pass

  @staticmethod
  def calc(data):
    peak = np.average(np.abs(data)) * 2
    bars = "#" * int(200 * peak / 2**16)
    return (peak, bars)
