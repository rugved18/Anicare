from django.contrib import admin
from .models import AnimalReport

class AnimalReportAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'location', 'animal_type', 'priority', 'latitude', 'longitude')

admin.site.register(AnimalReport, AnimalReportAdmin)
