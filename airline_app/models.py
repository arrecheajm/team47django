# type: ignore
# ^^^ disables pyright-extended's flaky type checking.
'''
16/4/2024 Added pax_demand function.
16/4/2024 Added airports model.
14/4/2024 Added airlines model.
12/4/2024 Added fleets model.
13/4/2024 Added random_aircraft_registration_generator function.
'''
from django.db.models import Sum
from datetime import datetime, time
from datetime import date
from datetime import timedelta
from django.contrib.auth import validators
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from haversine import haversine, Unit
from django.db import transaction
from django.db import models
from django.db.models.fields import BooleanField
from django.contrib.auth.models import User
from django.utils import timezone

import random
import string


def random_airline_designator_generator():
  letters = string.ascii_uppercase
  return ''.join(random.choice(letters) for _ in range(2))


def pax_demand(rating_decimal: Decimal,
               price_decimal: Decimal,
               base_price=300,
               base_pax_demand=400):
  # This function calculates the number of buyers for a ticket based on
  # an airline's customer rating and the price of a ticket for that flight.
  # The formula is based on a supply and demand curve that has its
  # equilibrium at the given base pax demand and base price for an airline with
  # a perfect rating of 1.
  rating = float(rating_decimal)
  price = float(price_decimal)

  if rating == 0:
    return 0
  pax_demand = int((price - (base_price + 150) * rating) /
                   (-1 * rating * (1 / (base_pax_demand / 150))))
  if pax_demand < 0:
    return 0
  else:
    return pax_demand


def random_4digit_integer():
  integers = string.digits
  return ''.join(random.choice(integers) for _ in range(4))


def random_aircraft_registration_generator():
  letters = string.ascii_uppercase
  prefix = 'N-'  #N is for airacraft registered in the US
  suffix = ''.join(random.choice(letters) for _ in range(5))
  return prefix + suffix


def airline_active_fleet(self, airline=None):
  return self.Fleet.objects.filter('airline' == airline, 'is_active' == True)


class AirlineCost(models.Model):
  flight_hours_year = models.FloatField(default=800.00,
                                        verbose_name='Flight Hours/Year')
  captain_salary = models.FloatField(default=200000.00,
                                     verbose_name="Captain's Salary $")
  first_officer_salary = models.FloatField(
      default=110000.00, verbose_name="First Officer's Salary $")
  flight_attendant_salary = models.FloatField(
      default=55000.00, verbose_name="Flight Attendant's Salary $")

  # crew cost.
  def crew_cost(self, hours: Decimal) -> Decimal:
    captain_rate = self.captain_salary / self.flight_hours_year
    fo_rate = self.first_officer_salary / self.flight_hours_year
    fa_rate = self.flight_attendant_salary / self.flight_hours_year
    return Decimal((captain_rate + fo_rate + fa_rate) * float(hours))


class Economy(models.Model):
  # Jet-A (airliner fuel) price per lb in USD
  gas_price = models.DecimalField(
      max_digits=12,
      decimal_places=4,
      default=1.100000,
      verbose_name='Gas Price ($/lb)',
  )
  initial_ticket_price = models.FloatField(
      default=300.00,
      verbose_name='Initial ticket price ($/ticket)',
  )
  initial_pax_demand = models.FloatField(
      default=400.00,
      verbose_name='Initial PAX demand',
  )


class Airport(models.Model):
  # Name
  name = models.CharField(max_length=64)
  # Location. A 3-letter IATA code.
  location = models.CharField(max_length=3)
  # Rating.
  rating = models.DecimalField(
      max_digits=4,
      decimal_places=3,
      default=0.75,
      validators=[MinValueValidator(0.000),
                  MaxValueValidator(1.000)])
  # Longitude. Decimal degress
  latitude = models.DecimalField(max_digits=9, decimal_places=6)
  longitude = models.DecimalField(max_digits=9, decimal_places=6)
  # Elevation FAMSL (feet above mean sea level)
  elevation = models.IntegerField()
  # Arrival delay. Minutes aircraft arivals are delay.
  arrival_delay = models.IntegerField(default=0)
  # Departure delay. Minutes aircraft departures are delay.
  departure_delay = models.IntegerField(default=0)
  # Timezone. Hours offset from UTC time
  timezone = models.IntegerField()
  # dst. Whether or not daylight savings is active in the timezone.
  dst = models.BooleanField(default=False)

  def __str__(self):
    return self.location


class Aircraft(models.Model):
  # model = Name of aircraft
  model = models.CharField(max_length=100)
  # price_millions = Cost in millions USD to purchase aircraft
  price_millions = models.DecimalField(default=100,
                                       max_digits=8,
                                       decimal_places=2)
  # image
  image = models.ImageField(upload_to='aircraft_images/',
                            default='default.png')
  # seats = # of seats on aircraft
  seats = models.IntegerField()
  # range = Aircraft range distance (miles)
  range = models.IntegerField(verbose_name='Range (miles)')
  # fuel burn = lbs of fuel consumed per mile (lbs/miles)
  fuel_burn = models.DecimalField(max_digits=8,
                                  decimal_places=2,
                                  verbose_name='Fuel burn (lbs/miles)')
  # fuel per seat = Fuel efficiency per seat (mpg_us)
  # fuel_per_seat = models.DecimalField(max_digits=8, decimal_places=2)
  # cruise speed in (mph)
  cruise_speed = models.PositiveSmallIntegerField(
      default=500, verbose_name='Cruise speed (mph)')
  # pax comfort. Relative and subjective measure.
  # A real number in the interval [0,1]
  # larger => better as in general less noise, more space
  #     e.g.
  #     Airbus 380 or Boeing 787 = 0.9999 pax_comfort,
  #     Cessna 208 = 0.25 pax_comfort,
  #     Parachute = 0 pax_comfort.
  # newer design => better
  pax_comfort = models.DecimalField(default=0.8,
                                    max_digits=3,
                                    decimal_places=2)

  def __str__(self):
    return self.model


class Airline(models.Model):
  # A airline must be linked to a user.
  # A 1-to-many relationship. A airline has only one user,
  # but a user may have zero or more airlines.
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  # airline's name
  name = models.CharField(max_length=16, default='Acme Airlines')
  # current day.
  current_day = models.PositiveIntegerField(default=0)
  # airline designator.
  # Two uppercase letters that prefix all the airline's flights
  designator = models.CharField(max_length=2,
                                default=random_airline_designator_generator)
  # airline homebase
  # homebase = models.CharField(max_length=3, default='DFW')
  homebase = models.ForeignKey(Airport,
                               on_delete=models.SET_NULL,
                               null=True,
                               default=1)
  # airline's cost model
  cost_model = models.ForeignKey(AirlineCost,
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 default=1)
  # airline's total revenue in USD
  revenue = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
  # airline's total costs in USD
  costs = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
  # airline's customer rating. A real number [0, 1]
  # 0 : zero tickets will sell at any price (user has lost the simulation)
  # 1 : the max number of tickets will sell based on the pax_demand fn.
  rating = models.DecimalField(
      max_digits=4,
      decimal_places=3,
      default=0.75,
      validators=[MinValueValidator(0.000),
                  MaxValueValidator(1.000)])

  # Profit. Derived field (not kept in db)
  def profit(self):
    return self.revenue - self.costs

  # inc_day. Increase the airline's current day by 1.
  def inc_day(self):
    self.current_day += 1
    self.save()

  def __str__(self):
    return self.name


class Fleet(models.Model):
  registration = models.CharField(
      max_length=8,
      default=random_aircraft_registration_generator,
      help_text='''<br>A code unique to a single aircraft and
      marked on it's exterior.''',
  )
  is_active = models.BooleanField(
      default=True,
      verbose_name='Active',
      help_text=
      '''<br>Designates whether this fleet aircraft should be treated as active.
        Uncheck instead of deleting aircarft.''',
  )
  # A fleet aircraft must be linked to a airline.
  # A 1-to-many relationship i.e. A fleet aircraft belongs to only one airline,
  # but an airline may have zero or more fleet aircraft.
  airline = models.ForeignKey(Airline, on_delete=models.CASCADE, default=1)
  # A fleet aircraft must be linked to a aircraft model.
  # A 1-to-many relationship. A fleet aircraft has only one model,
  # but a model may be in use by many fleet aircraft.
  aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
  # The total number of hours the fleet aircraft has flown.
  operating_hours = models.DecimalField(max_digits=16,
                                        decimal_places=2,
                                        default=0)
  # one cycle is one complete flight operation.
  # i.e. one takeoff and landing
  cycles = models.IntegerField(default=0)
  # Location. An airport object.
  location = models.ForeignKey(Airport, on_delete=models.CASCADE, default=1)
  # Manufature
  manufacture_date = models.DateField(default=date.today)
  # livery
  livery_title = models.CharField(max_length=32, default="Factory finish")
  livery = models.ImageField(upload_to='livery_images/', default='default.png')
  # Last landing date and time
  last_landing_datetime = models.DateTimeField(default=timezone.now)
  # maintenance. Sim days until due
  next_a_check = models.PositiveIntegerField(
      default=70, verbose_name='Next A-Check (days)')
  next_b_check = models.PositiveIntegerField(
      default=280, verbose_name='Next B-Check (days)')
  next_c_check = models.PositiveIntegerField(
      default=560, verbose_name='Next C-Check (days)')
  next_d_check = models.PositiveIntegerField(
      default=2800, verbose_name='Next D-Check (days)')

  def __str__(self):
    return self.registration


class Flight(models.Model):
  # Airline operating the flight
  airline = models.ForeignKey(Airline, on_delete=models.CASCADE, default=1)
  # Flight number.
  # Prefix is the airline's designator
  # Suffix is a 4 digit random integer
  # e.g. WN 4173, AA 3122
  number = models.CharField(max_length=7,
                            blank=True,
                            verbose_name='Flight number')
  # Aircraft
  aircraft = models.ForeignKey(Fleet, on_delete=models.CASCADE, blank=False)
  # Origin
  origin = models.ForeignKey(Airport,
                             on_delete=models.CASCADE,
                             blank=False,
                             related_name='origin_choices')
  # Destination
  destination = models.ForeignKey(Airport,
                                  on_delete=models.CASCADE,
                                  related_name='destination_choices')
  # Distance. The great circle distance between
  # the origin and destination in miles. Accuracy is 0.5 feet.
  # Auto calculated when save(self, *args, **kwargs) is invoked.
  distance = models.DecimalField(max_digits=12,
                                 decimal_places=4,
                                 default=0.0000)
  # Day
  day = models.PositiveIntegerField(default=0)
  # crew.
  captains = models.PositiveIntegerField(default=1)
  first_officers = models.PositiveIntegerField(default=1)
  flight_attendants = models.PositiveIntegerField(default=2)
  # Scheduled departure time in UTC
  sch_departure_time = models.TimeField()
  # Actual departure time in UTC
  act_departure_time = models.TimeField(default='00:00:00')
  # Schduled arrival time in UTC
  sch_arrival_time = models.TimeField()
  # Actual arrival time in UTC
  act_arrival_time = models.TimeField(default='00:00:00')
  # Ticket price in USD
  ticket_price = models.DecimalField(max_digits=8, decimal_places=2)
  # Tickets sold
  tickets_sold = models.PositiveIntegerField(default=0)
  # Revenue from the flight
  # Calculated at save time as ticket_price * tickets_sold
  revenue = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
  # Cost of the flight
  fuel_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
  crew_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
  cost = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
  # is_complete. True when the flight has been compeleted.
  is_complete = BooleanField(default=False)
  # is_cancelled. True when the flight has been cancelled.
  is_canceled = BooleanField(default=False, verbose_name='Cancel')
  # flight rating. A real number in the interval [0,1]
  # 1 = perfect
  # 0 = everyone is dead
  rating = models.DecimalField(max_digits=4, decimal_places=3, default=0.75)

  # DERIVED FIELDS (not stored in db)
  def profit(self):
    return f"{round(self.revenue - self.cost, 2):,}"

  # override class save() method to assign fields that require a complete entry.
  def save(self, *args, **kwargs):
    # If a flight number is not provided (blank=True), assign one.
    if not self.number:
      self.number = self.airline.designator + " " + random_4digit_integer()
    # assign the great circle distance between the origin and destination.
    origin = Airport.objects.get(pk=self.origin.id)
    origin_coords = (origin.latitude, origin.longitude)
    destination = Airport.objects.get(pk=self.destination.id)
    destination_coords = (destination.latitude, destination.longitude)
    self.distance = haversine(origin_coords, destination_coords, Unit.MILES)
    super().save(*args, **kwargs)

  def __str__(self):
    return self.number


# class AirlineCosts(models.Model):
# Strategy. A name for the cost strategy. e.g. ultra-low-cost, low-cost, hybrid
# strategy = models.CharField(max_length=32)
# Fuel cost ($/lb). All pay the same price
# fuel_cost = models.ForeignKey(Economy, on_delete=models.CASCADE)


class AircraftFeedback(models.Model):
  message = models.CharField(max_length=200)


class SimEngine(models.Model):
  # User. One record(simEngine) for each user.
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  # sim_day. The current day number inside the sim.
  current_day = models.PositiveIntegerField(default=0)

  @transaction.atomic
  def process_day(todays_flights, airline):
    print(f"{todays_flights=}")
    print(f"{airline=}")
    for flight in todays_flights:
      if flight.is_canceled:
        continue
      print(f"{flight.number=}")
      # set day of flight
      flight.day = airline.current_day
      # actual departure time
      sch_departure_time = flight.sch_departure_time
      departure_delay = flight.origin.departure_delay
      sch_departure_datetime = datetime.combine(datetime.today(),
                                                sch_departure_time)
      act_departure_datetime = sch_departure_datetime + timedelta(
          minutes=departure_delay)
      act_departure_time = act_departure_datetime.time()
      flight.act_departure_time = act_departure_time
      # actual arrival time
      distance = flight.distance
      cruise_speed = flight.aircraft.aircraft.cruise_speed
      climb_descend_duration = 60
      onroute = timedelta(hours=float(distance / cruise_speed))
      onroute += timedelta(minutes=climb_descend_duration)
      arrival_delay = timedelta(minutes=flight.destination.arrival_delay)
      total_duration = onroute + arrival_delay
      act_arrival_datetime = act_departure_datetime + total_duration
      flight.act_arrival_time = act_arrival_datetime.time()
      # flight rating
      airline_rating = flight.airline.rating
      aircraft_rating = flight.aircraft.aircraft.pax_comfort
      origin_rating = flight.origin.rating
      destination_rating = flight.destination.rating
      average_rating = (airline_rating + aircraft_rating + origin_rating +
                        destination_rating) / 4
      flight.rating = average_rating
      #tickets sold and flight revenue
      act_demand = pax_demand(flight.airline.rating, flight.ticket_price)
      print(f"{act_demand=}")
      if flight.aircraft.aircraft.seats < act_demand:
        flight.tickets_sold = flight.aircraft.aircraft.seats
      else:
        flight.tickets_sold = act_demand
      flight.revenue = flight.ticket_price * flight.tickets_sold
      # fuel cost
      economy = Economy.objects.first()
      flight.fuel_cost = flight.distance * flight.aircraft.aircraft.fuel_burn * economy.gas_price
      flight.cost = flight.fuel_cost
      # crew cost
      duration_hours = Decimal(total_duration.total_seconds() / 3600)
      flight.crew_cost = flight.airline.cost_model.crew_cost(duration_hours)
      flight.cost += flight.crew_cost
      # update airline revenue and costs
      airline.revenue += flight.revenue
      airline.costs += flight.cost
      airline.save()
      # update fleet aircraft used for the flight
      fleet = Fleet.objects.get(id=flight.aircraft.id)
      print(f"{fleet=}")
      fleet.operating_hours += Decimal(total_duration.total_seconds() / 3600)
      fleet.next_a_check -= 1 if fleet.next_a_check > 0 else 0
      fleet.next_b_check -= 1 if fleet.next_b_check > 0 else 0
      fleet.next_c_check -= 1 if fleet.next_c_check > 0 else 0
      fleet.next_d_check -= 1 if fleet.next_d_check > 0 else 0
      fleet.cycles += 1
      fleet.location = flight.destination
      # increment airline's day
      airline.inc_day()

      airline.save()
      fleet.save()
      # TODO mark flight as complete
      flight.save()

    print(f"{todays_flights=}")
    return todays_flights
