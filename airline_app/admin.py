from .models import AirlineCost
from .models import SimEngine
from .models import Economy
from .models import Flight
from .models import Airport
from .models import Airline
from .models import Fleet
from django.contrib import admin
from .models import Aircraft, AircraftFeedback
from import_export.admin import ImportExportModelAdmin

# Register your models here.

admin.site.register(AirlineCost)
admin.site.register(SimEngine)
admin.site.register(AircraftFeedback)

class EconomyAdmin(ImportExportModelAdmin, admin.ModelAdmin):

  class Meta:
    model = Economy

admin.site.register(Economy, EconomyAdmin)

class FleetAdmin(ImportExportModelAdmin, admin.ModelAdmin):

  class Meta:
    model = Fleet

admin.site.register(Fleet, FleetAdmin)


class AirlineAdmin(ImportExportModelAdmin, admin.ModelAdmin):

  class Meta:
    model = Airline


admin.site.register(Airline, AirlineAdmin)


class AirportAdmin(ImportExportModelAdmin, admin.ModelAdmin):

  class Meta:
    model = Airport


admin.site.register(Airport, AirportAdmin)


class FlightAdmin(ImportExportModelAdmin, admin.ModelAdmin):

  class Meta:
    model = Flight


admin.site.register(Flight, FlightAdmin)


class AircraftAdmin(ImportExportModelAdmin, admin.ModelAdmin):

  class Meta:
    model = Aircraft


admin.site.register(Aircraft, AircraftAdmin)
