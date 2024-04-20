'''
## [1.0.0] - 2024-02-20
### Added
- UserCreationForm
'''
from django import forms
from django.forms import modelformset_factory
from .models import Flight
from .models import AircraftFeedback
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = UserCreationForm.Meta.fields + ("email", )


class FlightForm(ModelForm):

  class Meta:
    model = Flight
    fields = [
        'number', 'aircraft', 'origin', 'destination', 'sch_departure_time',
        'sch_arrival_time', 'ticket_price', 'is_canceled'
    ]


class AircraftFeedbackForm(ModelForm):

  class Meta:
    model = AircraftFeedback
    fields = ('message', )


FlightFormSet = modelformset_factory(Flight, form=FlightForm, extra=1)
