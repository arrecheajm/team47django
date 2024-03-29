'''
## [1.0.1] - 2024-03-25
### Added
- aircraft loopup page
'''
'''
## [1.0.0] - 2024-03-22
### Added
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
from verify_email.email_handler import send_verification_email
from django_project.settings import DEFAULT_FROM_EMAIL
from django.core.mail import send_mail
from django.contrib.auth import login
from airline_app.forms import CustomUserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.models import User
import re
from .models import Aircraft
from airline_app.forms import AircraftFeedbackForm
from django.forms import modelformset_factory


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
  AirCraftFeedbackFormSet = modelformset_factory(AircraftFeedbackForm,
                                                 fields=["message"])
  if request.method == "POST":
    formset = AirCraftFeedbackFormSet(request.POST, request.FILES)
    if formset.is_valid():
      formset.save()
      # do something.
  else:
    formset = AirCraftFeedbackFormSet()
  return render(request, "aircraft/feedback.html", {"formset": formset})


# Create your views here.
def about_team(request):
  return render(request, 'about_team.html')


def onboarding(request):
  return render(request, 'onboarding.html')


def dashboard(request):
  return render(request, 'dashboard.html')


def register(request):
  if request.method == 'GET':
    return render(request, 'registration/register.html',
                  {'form': CustomUserCreationForm})
  elif request.method == 'POST':
    form = CustomUserCreationForm(request.POST)

    username = request.POST.get('username')
    user = User.objects.filter(username=username)
    if user.exists():
      return render(request, 'registration/registration_problem.html',
                    {'message': username + ' is already taken.'})

    email = request.POST.get('email')
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
      return render(request, 'registration/registration_problem.html',
                    {'message': email + ' - is not a valid email format'})
    user_by_email = User.objects.filter(email=email)
    if user_by_email.exists():
      return render(request, 'registration/registration_problem.html',
                    {'message': email + ' is already taken.'})

    password1 = request.POST.get('password1')
    password2 = request.POST.get('password2')
    if password1 != password2:
      return render(request, 'registration/registration_problem.html',
                    {'message': 'Passwords do not match.'})
    password_length = len(request.POST.get('password1'))
    if password_length < 8:
      return render(request, 'registration/registration_problem.html',
                    {'message': 'Password is too short. Minimum length is 8'})

    if form.is_valid():
      inactive_user = send_verification_email(request, form)
      # user = form.save()
      # login(request, inactive_user)
      send_welcome_email(request)
      return render(request, 'onboarding.html', {'email': email})
    else:
      return redirect(reverse('register'))


def send_welcome_email(request):
  username = request.POST.get('username')
  subject = 'Welcome to Airline Simulator'
  message = f'Welcome {username}. Your account has been successfully created. You can start using the Airline Simulator.'
  from_email = f'Airline Admin <{DEFAULT_FROM_EMAIL}>'
  recipient_list = [request.POST.get('email')]
  send_mail(subject, message, from_email, recipient_list, fail_silently=True)
