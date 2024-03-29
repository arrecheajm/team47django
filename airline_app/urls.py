'''
## [1.0.1] - 2024-03-25
### Added
- Aircraft lookup page
'''
'''
## [1.0.0] - 2024-02-24
### Added
- about team.
- register path.
- accoutns path.
- dashboard path.
### Changed
- "register" path to "registration/register/"
'''

from django.urls import path, include
from . import views
"""
URL configuration for airline_app.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

urlpatterns = [
    path('verification/', include('verify_email.urls')),
    path('about_team/', views.about_team, name='about_team'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('registration/register/', views.register, name='register'),
    path("aircraft/search/", views.AircraftFilterView, name='aircraft_search'),
    path("aircraft/feedback/",
         views.AircraftFeedbackForm,
         name='aircraft_feedback'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.dashboard, name='dashboard'),
]
