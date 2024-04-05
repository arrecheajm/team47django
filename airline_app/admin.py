from django.contrib import admin
from .models import Aircraft, AircraftFeedback
from import_export.admin import ImportExportModelAdmin


# Register your models here.
class aircraftAdmin(ImportExportModelAdmin, admin.ModelAdmin):
  ...


admin.site.register(Aircraft, aircraftAdmin)
admin.site.register(AircraftFeedback)
