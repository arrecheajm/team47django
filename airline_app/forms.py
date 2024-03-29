'''
## [1.0.0] - 2024-02-20
### Added
- UserCreationForm
'''

from django.contrib.auth.forms import UserCreationForm
from .models import AircraftFeedback
from django import forms


class CustomUserCreationForm(UserCreationForm):

  class Meta(UserCreationForm.Meta):
    fields = UserCreationForm.Meta.fields + ("email", )


class AircraftFeedbackForm(forms.ModelForm):

  class Meta:
    model = AircraftFeedback
    fields = ('message', )
