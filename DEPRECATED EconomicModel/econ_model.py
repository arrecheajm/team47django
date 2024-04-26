from econ_indicators import Econ_Indicators
import random


class Econ_Model:

  def __init__(self, region):
    self.indicators = Econ_Indicators()
    self.infl_rate = self.set_infl_rate(region)
    self.prev_infl_rate = self.set_infl_rate(region)

  def set_infl_rate(self, region):
    col_name = 'values.PCPIPCH.' + region + '.2024'
    return self.indicators.inflation_df[col_name][0]

  def update_infl_rate(self):
    deviation = self.infl_rate / self.prev_infl_rate
    attract = .5 * deviation
    r = random.uniform(0, 1)

    self.prev_infl_rate = self.infl_rate

    if r < attract:
      self.infl_rate += .05
    else:
      self.infl_rate -= .05
    self.infl_rate = round(self.infl_rate, 2)


if __name__ == "__main__":
  e_model = Econ_Model('USA')
  for x in range(200):
    e_model.update_infl_rate()
    if x > 180:
      print(e_model.infl_rate)
