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
from django.core.validators import EmailValidator
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
  email = forms.EmailField(validators=[EmailValidator(message='Enter a valid email address.')])
  
  class Meta(UserCreationForm.Meta):
    fields = UserCreationForm.Meta.fields + ("email", )

  def clean_email(self):
    email = self.cleaned_data.get('email')
    if User.objects.filter(email=email).exists():
      raise forms.ValidationError("This email address is already in use. Please use a different email.")
    return email
    
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].label = "Username"
    self.fields['username'].help_text = ""
    self.fields['password2'].help_text = ""
    


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
    # fields = '__all__'
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
        # 'is_canceled': forms.HiddenInput(),
    }

  def __init__(self, *args, airline=None, **kwargs):
    super().__init__(*args, **kwargs)
    if airline:
      self.fields['aircraft'].queryset = Fleet.objects.filter(
          airline=airline).filter(is_active=True)
      #new
      self.fields['airline'].initial = airline


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
