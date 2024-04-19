'''
## [1.0.0] - 2024-02-20
### Added
- UserCreationForm
'''

from django.contrib.auth.forms import UserCreationForm
from .models import AircraftFeedback, Flight
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = UserCreationForm.Meta.fields + ("email", )


class FlightForm(ModelForm):

  class Meta:
    model = Flight
    fields = [
        'aircraft', 'origin', 'destination', 'sch_arrival_time',
        'sch_departure_time', 'ticket_price'
    ]


class AircraftFeedbackForm(ModelForm):

  class Meta:
    model = AircraftFeedback
    fields = ('message', )
