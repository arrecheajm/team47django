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

admin.site.register(SimEngine)
admin.site.register(Economy)
admin.site.register(Flight)
admin.site.register(Airport)
admin.site.register(Airline)
admin.site.register(Fleet)
class aircraftAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  ...


admin.site.register(Aircraft, aircraftAdmin)
admin.site.register(AircraftFeedback)


