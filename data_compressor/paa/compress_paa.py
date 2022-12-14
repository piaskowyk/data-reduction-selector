from data_compressor.compressor import Compressor
from data_type import Measurement

# uniform, fixed points count
# PAA - Piecewise Polynomial Approximation
# kais_2000.pdf https://jmotif.github.io/sax-vsm_site/morea/algorithm/PAA.html
class CompressPAA(Compressor):

  def __init__(self, config = {}) -> None:
    super().__init__()
    compress_ratio = config.get('compress_ratio', 0.5)
    self.config = {
      'compress_ratio': compress_ratio,
    }

  def compress(self):
    tmp = len(self.compressed_data)
    data_size = len(self.original_data)
    if data_size < 2:
      self.compressed_data = self.original_data[:]
      return
    chunk_count = int(data_size * self.config['compress_ratio'] / 2)
    if chunk_count == 0:
      self.compressed_data = self.original_data[:]
    x_first = self.original_data[0].timestamp
    x_last = self.original_data[data_size - 1].timestamp
    chunk_size = (x_last - x_first) / chunk_count

    series = []
    stop = False
    last_checked_index = 0
    for i in range(chunk_count):
      current_series = []
      while (x_first + (i + 1) * chunk_size) > self.original_data[last_checked_index].timestamp:
        current_series.append(self.original_data[last_checked_index].value)
        last_checked_index += 1
        if last_checked_index >= data_size:
          stop = True
          break
      if len(current_series) > 0:
        series.append(sum(current_series) / len(current_series))
      if stop:
        break

    for i, value in enumerate(series):
      self.compressed_data.append(Measurement(value, x_first + i * chunk_size))
      self.compressed_data.append(Measurement(value, x_first + (i + 1) * chunk_size))

    if len(self.compressed_data) > len(self.original_data):
      print(tmp, len(self.original_data), len(self.compressed_data), len(series), chunk_count, data_size, self.config['compress_ratio'])
      # self.vizualize()
