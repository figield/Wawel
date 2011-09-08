from django.db import models

class Measure(models.Model):
    Name = models.CharField(max_length=10)
    Value =  models.FloatField()
    MeasureDate = models.DateTimeField('Measure Date')
    UnitOfMeasure = models.CharField(max_length=3)
    def __unicode__(self):
        return self.MeasureDate.strftime("%Y/%m/%d %H:%M ") + self.Name

class MeasureMonth(models.Model):
    Month = models.CharField(max_length=7)
    def __unicode__(self):
        return self.Month
