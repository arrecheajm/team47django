# type: ignore
from django.db.transaction import commit
from .models import random_4digit_integer, random_aircraft_registration_generator, random_airline_designator_generator
from .models import SimEngine
from .models import Airport
from .models import Airline
from .models import Fleet
from .models import Flight
from .models import Aircraft
from .models import AircraftFeedback
from .forms import AirlineForm, FleetFormSet, FlightFormSet
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from verify_email.email_handler import send_verification_email
from django_project.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.contrib.auth import login
from airline_app.forms import CustomUserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
import re
from airline_app.forms import AircraftFeedbackForm
from django.forms import modelformset_factory
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Avg, Sum, Count, F
from django.db.models.functions import TruncDay
from datetime import datetime, timedelta


def get_current_airline(request):
  try:
    current_user_id = request.user.id
    return Airline.objects.get(user_id=current_user_id)
  except:
    return None


def airports(request):
  airports = Airport.objects.all()
  if request.method == 'GET':
    return render(request, 'airports/overview.html', {'airports': airports})


@login_required
def aircraft(request):
  aircrafts = Aircraft.objects.all()
  if request.method == 'GET':
    return render(request, 'aircraft/overview.html', {'aircrafts': aircrafts})
  elif request.method == 'POST':
    clicked_aircraft = request.POST.get('clicked_aircraft')
    aircraft_to_add = Aircraft.objects.get(id=clicked_aircraft)
    airline = get_current_airline(request)
    new_fleet_entry = Fleet(airline=airline, aircraft=aircraft_to_add)
    new_fleet_entry.save()
    return redirect(reverse('fleet'))


@login_required
def airline(request):
  airline = get_current_airline(request)
  print(f"{request=}")
  if request.method == 'POST':
    if 'submit' in request.POST:
      post_form = AirlineForm(request.POST, instance=airline)
      print(f"{post_form=}")
      if post_form.is_valid():
        post_form.save()
    elif 'analytics' in request.POST:
      return redirect('airline_analytics')
  return render(request, 'airline/overview.html', {
      'airline': AirlineForm(instance=airline),
      'airline_obj': airline
  })


@login_required
def airline_analytics(request):

  # ***** Airline Data *****
  # Get airline
  airline = get_current_airline(request)
  aircrafts = Aircraft.objects.all()

  # Calculate date
  current_day = airline.current_day
  analytics_start_day = current_day - 30

  # Get flights
  # flights = Flight.objects.filter(is_complete=True, airline=airline, day__gt=analytics_start_day, day__lte=current_day)
  flights = Flight.objects.all()
  # flights = Flight.objects.filter(airline=airline, day__gt=analytics_start_day, day__lte=current_day)  #****CHANGE TO SPECIFIC AIRLINE****  # Dates for calculations

  # ***** Metrics Calcualtion *****

  #Operation Performance
  performance_data = {}
  #Flights Completed
  # performance_data['number_flights_completed'] = flights.filter(is_complete=True).count()
  performance_data['number_flights_completed'] = flights.count()
  #Average Distance
  performance_data['average_distance'] = flights.aggregate(
      Avg('distance'))['distance__avg']

  #Revenue $ Costs
  performance_data['total_revenue'] = flights.aggregate(
      Sum('revenue'))['revenue__sum']
  performance_data['total_cost'] = flights.aggregate(Sum('cost'))['cost__sum']
  performance_data['profitability'] = performance_data[
      'total_revenue'] - performance_data['total_cost']
  number_of_delayed_flights = 0
  # #Load Factor
  for flight in flights:
    tickets_sold = flight.tickets_sold
    total_seats = flight.aircraft.aircraft.seats  # Make sure 'aircraft' is the related name for the Aircraft model
    flight.load_factor = (tickets_sold / total_seats
                          ) * 100 if total_seats else 0  # Flight load factor
    flight.profit = flight.revenue - flight.cost  # Flight profit
    now = datetime.now()
    act_time = datetime.combine(now.date(), flight.act_departure_time)
    sched_time = datetime.combine(now.date(), flight.sch_departure_time)

    # Check if the actual departure time is at least 15 minutes later than scheduled time
    flight.delayed = (act_time - sched_time > timedelta(minutes=15))
    if flight.delayed:
      number_of_delayed_flights += 1

  total_load_factor = sum(flight.load_factor for flight in flights)
  average_load_factor = total_load_factor / len(flights) if flights else 0
  performance_data['average_load_factor'] = average_load_factor

  # Flight Performance
  performance_data['cancelled_flights'] = flights.filter(
      is_canceled=True).count()
  performance_data['delayed_flights'] = number_of_delayed_flights
  performance_data['delay_rate'] = (
      performance_data['delayed_flights'] /
      performance_data['number_flights_completed'])
  performance_data['average_flight_rating'] = flights.aggregate(Avg('rating'))

  # # Aggregate data for charts
  daily_flights = flights.values('day').annotate(
      count=Count('id')).order_by('day')
  destination_distribution = flights.values('destination').annotate(
      total=Count('id')).order_by('-total')

  print(f"{request=}")
  # if request.method == 'POST':

  context = {
      'airline': airline,
      'flights': flights,
      'performance_data': performance_data,
      'daily_flights': list(daily_flights),
      'destination_distribution': list(destination_distribution)
  }

  return render(request, 'airline/analytics.html', context)


@login_required
def fleet(request):
  # print(f'\n{request.GET=}')
  # print(f'\n{request.POST=}')
  # print(f"\nPOST...{request.POST.get('only_active_switch')=}")
  only_active = request.POST.get('only_active_switch')
  # print(only_active)
  airline = get_current_airline(request)
  if only_active:
    fleet = Fleet.objects.filter(airline=airline)
  else:
    fleet = Fleet.objects.filter(airline=airline, is_active=True)
  if not fleet:
    formset = None
  else:
    formset = FleetFormSet(queryset=fleet)
  context = {'formset': formset, 'only_active_switch': only_active}
  if request.method == 'GET':
    return render(request, 'fleet/overview.html', context)
  elif request.method == 'POST':
    # if 'only_active_switch' in request.POST:
    if 'add' in request.POST:
      print('add')
      return redirect('aircraft')
    elif 'save' in request.POST:
      formset = FleetFormSet(request.POST)
      if formset.is_valid():
        print(f'{formset.is_valid()=}')
        print(f'{formset.has_changed()=}')
        formset.save()
      context = {'formset': formset, 'only_active_switch': only_active}
      return render(request, 'fleet/overview.html', context)
    elif 'details' in request.POST:
      print(f"details")
      id = request.POST.get('details')
      fleet_aircraft = Fleet.objects.get(id=id)
      print(fleet_aircraft)
      return redirect('fleet')
    else:
      context = {'formset': formset, 'only_active_switch': only_active}
      return render(request, 'fleet/overview.html', context)


@login_required
def flights(request):
  airline = get_current_airline(request)
  flights = Flight.objects.filter(airline=airline)
  
  formset = FlightFormSet(
      queryset=flights,
      airline=airline,
  )
  if request.method == 'POST':
    print(f'{request.POST=}')
    formset = FlightFormSet(request.POST, airline=airline)
    if 'save' in request.POST:
      for form in formset.forms:
        if form.has_changed() and form.is_valid():
          form.save()
      return redirect('flights')

    if 'submit' in request.POST:
      flights_to_process = Flight.objects.filter(airline=airline,
                                                 is_canceled=False)
      processed_flights = SimEngine.process_day(flights_to_process, airline)
      return render(request, 'flights/results.html',
                    {'flights': processed_flights})

  # GET
  return render(request, 'flights/overview.html', {'formset': formset})


def is_valid_queryparam(param):
  return param != '' and param is not None


def AircraftFilterView(request):
  qs = Aircraft.objects.all()
  model_query = request.GET.get('model')
  seats_min_query = request.GET.get('seats_min')
  seats_max_query = request.GET.get('seats_max')
  sector_min_query = request.GET.get('sector_min')
  sector_max_query = request.GET.get('sector_max')
  fuelburn_min_query = request.GET.get('fuelburn_min')
  fuelburn_max_query = request.GET.get('fuelburn_max')
  fuelperseat_min_query = request.GET.get('fuelperseat_min')
  fuelperseat_max_query = request.GET.get('fuelperseat_max')

  if is_valid_queryparam(model_query):
    qs = qs.filter(model__icontains=model_query)

  if is_valid_queryparam(seats_min_query):
    qs = qs.filter(seats__gte=seats_min_query)

  if is_valid_queryparam(seats_max_query):
    qs = qs.filter(seats__lt=seats_max_query)

  if is_valid_queryparam(sector_min_query):
    qs = qs.filter(sector__gte=sector_min_query)

  if is_valid_queryparam(sector_max_query):
    qs = qs.filter(sector__lt=sector_max_query)

  if is_valid_queryparam(fuelburn_min_query):
    qs = qs.filter(fuelburn__gte=fuelburn_min_query)

  if is_valid_queryparam(fuelburn_max_query):
    qs = qs.filter(fuelburn__lt=fuelburn_max_query)

  if is_valid_queryparam(fuelperseat_min_query):
    qs = qs.filter(fuelperseat__gte=fuelperseat_min_query)

  if is_valid_queryparam(fuelperseat_max_query):
    qs = qs.filter(fuelperseat__lt=fuelperseat_max_query)

  context = {'queryset': qs}
  return render(request, "aircraft/search.html", context)


def AircraftFeedbackView(request):
  context = {'success': False}
  message = request.GET.get('feedback')
  if is_valid_queryparam(message):
    feedback = AircraftFeedback()
    feedback.message = message
    feedback.save()
    context['success'] = True

  return render(request, "aircraft/feedback.html", context)


def about_team(request):
  return render(request, 'about_team.html')


def onboarding(request):
  return render(request, 'onboarding.html')


@login_required
def dashboard(request):
  return render(request, 'dashboard.html')


def register(request):
  if request.method == 'GET':
    return render(request, 'registration/register.html',
                  {'form': CustomUserCreationForm})
  elif request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    #username
    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if user.exists():
      return render(request, 'registration/registration_problem.html',
                    {'message': username + ' is already taken.'})
    #email
    email = request.POST.get('email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      return render(request, 'registration/registration_problem.html',
                    {'message': email + ' - is not a valid email format'})
    user_by_email = User.objects.filter(email=email)
    if user_by_email.exists():
      return render(request, 'registration/registration_problem.html',
                    {'message': email + ' is already taken.'})
    #password
    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if password1 != password2:
      return render(request, 'registration/registration_problem.html',
                    {'message': 'Passwords do not match.'})
    password_length = len(request.POST.get('password1'))
    if password_length < 8:
      return render(request, 'registration/registration_problem.html',
                    {'message': 'Password is too short. Minimum length is 8'})
    #verification email
    if form.is_valid():
      inactive_user = send_verification_email(request, form)
      # user = form.save()
      # login(request, inactive_user)
      send_welcome_email(request)
      # create airline & fleet
      new_airline = Airline.objects.create(
          user=User.objects.get(username=username),
          name=inactive_user.username + ' Airlines',
          designator=random_airline_designator_generator(),
          homebase=Airport.objects.first(),
          revenue=0.00,
          costs=0.00,
          rating=0.750,
      )
      new_fleet = Fleet.objects.create(
          airline=new_airline,
          aircraft=Aircraft.objects.first(),
          location=Airport.objects.first(),
      )
      Flight.objects.create(
          airline=new_airline,
          aircraft=new_fleet,
          origin=Airport.objects.first(),
          destination=Airport.objects.last(),
          day=new_airline.current_day,
          sch_departure_time = '07:00',
          sch_arrival_time = '11:00',
          ticket_price = '150.00'
      )

      return render(request, 'onboarding.html', {'email': email})
    else:
      return redirect(reverse('register'))


def send_welcome_email(request):
  username = request.POST.get('username')
  subject = 'Welcome to Virtual Airline'

  message = f'''
  <p>
  Welcome to the skies of Virtual Airline, {username}!
  </p>
  Your account has been successfully created, and we’re excited to have you with us. You are now ready to navigate the complexities of airline management and take your understanding of the aviation industry to new heights.
  <p>
  <b>Getting Started</b>
  To kick off your journey, we’ve put together a few tips to help you take full advantage of all the features available:
  <ul>
  <li><b>Create Your First Flight:</b> Dive right into the simulation by scheduling your first flight. Visit your dashboard to get started.</li>
  <li><b>Explore the Fleet:</b> Check out our diverse range of aircraft and select the one that best fits your strategy.</li>
  <li><b>Simulation Guide:</b> Familiarize yourself with the ins and outs of the airline industry with our detailed simulation guide available <a href="https://33d2bef9-e4ad-48f3-9b55-d893e9b7764c-00-ft2ur0tp22md.worf.replit.dev/about_team/">here</a>.</li>
  </ul>
  <p>
  <b>Need Assistance?</b>
  <br>
  Our support team is here to help you every step of the way. If you have any questions or need assistance, feel free to reach out via our <a href="https://33d2bef9-e4ad-48f3-9b55-d893e9b7764c-00-ft2ur0tp22md.worf.replit.dev/about_team/">Support Center</a>.
  </p>
  <p>
  Thank you for choosing Virtual Airline. We can’t wait to see how high you’ll soar.
  </p>
  Happy flying!
  <br>
  The Virtual Airline Team
  '''

  from_email = f'Airline Admin <{DEFAULT_FROM_EMAIL}>'
  recipient_list = [request.POST.get('email')]
  send_mail(
      subject,
      message,
      from_email,
      recipient_list,
      html_message=message,
      fail_silently=True,
  )


'''
## [1.0.1] - 2024-03-25
### Added
- aircraft loopup page
'''
'''
## [1.0.0] - 2024-04-15 - Gavin
### Added
- added airport view.
- added fleet view.
- added verify email to register view.
- email already taken check.
- about team view.
- onboarding view.
- New account email.
- Postmark email service.
- passwords match check.
- password length check.
- invalid email check.
- username already taken check.
- register view.
- dashboard view.
### Changed
- "register.html" to "registration/register.html"
'''
