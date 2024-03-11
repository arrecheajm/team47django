from django.db import models


# --Aircraft Model--
# model = Name of aircraft
# seats = # of seats on aircraft
# sector = Aircraft flight distance
# fuelburn = kilograms of fuel burned per kilometer (kg/km)
# fuelperseat = Fuel efficiency per seat (L/kn)
class Aircraft(models.Model):
  model = models.CharField(max_length=100)
  seats = models.IntegerField()
  sector = models.IntegerField()
  fuelburn = models.DecimalField(max_digits=8, decimal_places=2)
  fuelperseat = models.DecimalField(max_digits=8, decimal_places=2)
