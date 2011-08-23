from django.db import models

class Measure(models.Model):
    Name = models.CharField(max_length=10)
    Value =  models.FloatField()
    MeasureDate = models.DateTimeField('Measure Date')
    UnitOfMeasure = models.CharField(max_length=3)
    #def __unicode__(self):
    #   return self.Name
