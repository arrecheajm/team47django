# This class contains all economic indicators and their values.

# Indicators include:
# - Inflation rate
# - Geopolitical events
# - Fuel price trends

# TO DO:
#Decide on data structure for geopolical events
# Find data source for fuel prices.
# Properly implement fuel price indicator
# Clean data frames

from sys import get_asyncgen_hooks
from urllib.request import urlopen
import json
import os
import pandas as pd

# https://www.imf.org/external/datamapper/PCPIPCH@WEO/OEMDC/ADVEC/WEOWORLD
inflation_src = 'https://www.imf.org/external/datamapper/api/v1/PCPIPCH'
# Need fuel source
fuel_src = ''


class Econ_Indicators:

  def __init__(self):
    if not os.path.isfile('cache/infl_data.csv'):
      self.cache_inflation_data()

    self.inflation_df = self.set_inflation_data()
    self.fuel_df = self.set_fuel_data()
    self.prev_geopolitical_event = None

  def set_inflation_data(self):
    return pd.read_csv('cache/infl_data.csv')

  def cache_inflation_data(self):
    print('Storing inflation data from:', inflation_src)
    response = urlopen(inflation_src)
    data_json = json.loads(response.read())
    df = pd.json_normalize(data_json)
    df.to_csv("cache/infl_data.csv", index=False)

  def set_fuel_data(self):
    #return pd.read_csv('cache/fuel_data.csv')
    return 60

  def cache_fuel_data(self):
    print('Storing fuel data from:', fuel_src)
    response = urlopen(fuel_src)
    data_json = json.loads(response.read())
    df = pd.json_normalize(data_json)
    df.to_csv("cache/fuel_data.csv", index=False)

  # type = Type of event
  # desc = Description of event
  # affected = Areas affected
  # impact = Variable associated with change to economic model. Should be elaborated on.
  def get_geopolical_event(self):
    type = ''
    desc = ''
    affected = []
    impact = 0
    self.prev_geopolitical_event = (type, desc, affected, impact)
    return self.prev_geopolitical_event


if __name__ == "__main__":
  e = Econ_Indicators()
  print(e.inflation_df['values.PCPIPCH.USA.2024'][0])
