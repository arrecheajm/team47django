'''
## [1.0.0] - 2024-02-20
### Added
- register view.
- dashboard view.
'''

from django.contrib.auth import login
from airline_app.forms import CustomUserCreationForm
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here. (newest at top)

def dashboard(request):
    return render(request, 'dashboard.html')

def register(request):
    if request.method == 'GET':
        return render(
            request,
            'register.html',
            {'form': CustomUserCreationForm}
        )
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('dashboard'))
            



