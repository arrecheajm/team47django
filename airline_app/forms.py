'''
## [1.0.0] - 2024-02-20
### Added
- UserCreationForm
'''
from django.contrib.auth import forms
from django import forms
from django.db.models.base import Model
from django.forms import modelformset_factory
from .models import Fleet, Flight
from .models import Airline
from .models import AircraftFeedback
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.forms import BaseModelFormSet


class CustomUserCreationForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = UserCreationForm.Meta.fields + ("email", )


class BaseFlightFormSet(BaseModelFormSet):

  def __init__(self, *args, airline=None, **kwargs):
    super().__init__(*args, **kwargs)
    self.airline = airline

  def get_form_kwargs(self, index):
    kwargs = super().get_form_kwargs(index)
    kwargs['airline'] = self.airline
    return kwargs


class FlightForm(ModelForm):

  class Meta:
    model = Flight
    fields = [
        'airline',
        'number',
        'aircraft',
        'origin',
        'destination',
        'sch_departure_time',
        'sch_arrival_time',
        'ticket_price',
        'is_canceled',
    ]
    widgets = {
        'airline': forms.HiddenInput(),
    }

  def __init__(self, *args, airline=None, **kwargs):
    super().__init__(*args, **kwargs)
    print(airline)
    if airline:
      self.fields['aircraft'].queryset = Fleet.objects.filter(
          airline=airline).filter(is_active=True)


FlightFormSet = modelformset_factory(
    model=Flight,
    form=FlightForm,
    formset=BaseFlightFormSet,
    extra=1,
)


class FleetForm(ModelForm):

  class Meta:
    model: Fleet
    fields = [
        'id',
        'registration',
        'livery_title',
        'is_active',
    ]


FleetFormSet = modelformset_factory(Fleet, form=FleetForm, extra=0)


class AirlineForm(ModelForm):

  class Meta:
    model = Airline
    fields = '__all__'
    widgets = {
        'user': forms.HiddenInput(),
        'current_day': forms.HiddenInput(),
        'revenue': forms.HiddenInput(),
        'costs': forms.HiddenInput(),
        'rating': forms.HiddenInput(),
        'cost_model': forms.HiddenInput(),
    }


class AircraftFeedbackForm(ModelForm):

  class Meta:
    model = AircraftFeedback
    fields = ('message', )
