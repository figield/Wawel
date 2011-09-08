from polls.models import Measure, MeasureMonth
from django.contrib import admin

class MeasureAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Value',  'UnitOfMeasure', 'MeasureDate')

admin.site.register(Measure,  MeasureAdmin)

class MeasureMonthAdmin(admin.ModelAdmin):
    list_display = ['Month']

admin.site.register(MeasureMonth,  MeasureMonthAdmin)
