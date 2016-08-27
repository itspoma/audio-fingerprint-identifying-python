from matplotlib import pyplot

class VisualiserPlot():
  def __init__(self):
    pass

  @staticmethod
  def show(data):
    pyplot.plot(data)
    pyplot.show()
