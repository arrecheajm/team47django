'''
## [1.0.0] - 2024-02-20
### Added
- register path.
- accoutns path.
- dashboard path.
'''

from django.urls import path, include
from airline_app.views import dashboard, register

urlpatterns = [
    path('register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', dashboard, name='dashboard'),
]
