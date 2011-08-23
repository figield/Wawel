from polls.models import Measure
from django.contrib import admin

class MeasureAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Value',  'UnitOfMeasure', 'MeasureDate')

admin.site.register(Measure,  MeasureAdmin)
