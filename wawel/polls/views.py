from polls.models import Measure
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from datetime import date, datetime
import random

# For Ajax requests
def update_temp(request, id):
    Temps = Measure.objects.filter( UnitOfMeasure = "C", 
                                    Name = id,  
                                    MeasureDate__year = date.today().year
                                    ).order_by('MeasureDate')
    if len(Temps) == 0:
        return render_to_response('polls/temp.html', {id:0})
    else:
        Temp = Temps[len(Temps) -1 ].Value 
        R = random.randint(-4, 4) * 0.1
        return render_to_response('polls/temp.html', {id:Temp + R})

def index(request):
    #TODO: take the last value from the separate record!!!!
    Outs = Measure.objects.filter( UnitOfMeasure = "C", 
                                   Name = "out",  
                                   MeasureDate__year = date.today().year
                                   ).order_by('MeasureDate')
    if len(Outs) == 0:
        Out = 0
    else:
        Out = Outs[len(Outs) -1 ].Value        

    Ins = Measure.objects.filter( UnitOfMeasure = "C", 
                                  Name = "saloon",  
                                  MeasureDate__year = date.today().year
                                  ).order_by('MeasureDate')
    if len(Ins) == 0:
        In = 0
    else:
        In = Ins[len(Ins) -1 ].Value
    
    Elecs = Measure.objects.filter( UnitOfMeasure = "kWh", 
                                    Name = "elec",  
                                    MeasureDate__year = date.today().year
                                    ).order_by('MeasureDate')
    if len(Elecs) == 0:
        Elec = 0
    else:
        Elec = Elecs[len(Elecs) -1 ].Value

    Thermals = Measure.objects.filter( UnitOfMeasure = "GJ", 
                                       Name = "thermal",  
                                       MeasureDate__year = date.today().year
                                       ).order_by('MeasureDate')
    if len(Thermals) == 0:
        ThermalGJ = 0
    else:
        ThermalGJ = Thermals[len(Thermals) -1 ].Value
    # Conversion base : 1 GJ = 277.77777777778 kWh 
    ThermalKWh = round(ThermalGJ * 277.77777777778, 2) 
    if Elec == 0:
        cop = 0
    else:
        cop = round(ThermalKWh / Elec, 1)


    # calculate day's costs of electricity usage
    day_cost = 5.0
    # calculate month's costs
    month_cost = 30 * 5.0

    return render_to_response('polls/index.html', 
                              {'out':Out,  
                               'saloon':In,  
                               'elec':Elec,  
                               'thermalgj':ThermalGJ,  
                               'thermalkwh':ThermalKWh, 
                               'cop':cop,
                               'day_cost':day_cost,
                               'month_cost':month_cost
                               })

def photos(request):
    return render_to_response('polls/photos.html', {})

def dayreport(request, year,  month, day):
    return render_to_response('polls/dayreport.html', 
                              {'year':year,
                               'month':month,
                               'day':day})

def monthreport(request, year,  month):
    days = []
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        Date = measure.MeasureDate.strftime("%Y/%m/%d")
        if Date not in days:
            days.append(Date)    
    return render_to_response('polls/monthreport.html', 
                              {'year':year,  
                               'month':month,
                               'days':days})

def yearreport(request):
    months = []
    for measure in Measure.objects.all():  #TODO: to trzeba przyspieszyc
        Date = measure.MeasureDate.strftime("%Y/%m")
        if Date not in months:
            months.append(Date)    
    return render_to_response('polls/yearreport.html', 
                              {'months':months})

#TODO: pomiary trzeba podzielic na podstrony
def all_measures(request):
    all_mesures = Measure.objects.all().order_by('MeasureDate')
    return render_to_response('polls/all_measures.html', 
                              {'all_mesures': all_mesures})

def detail(request, measure_id):
    try:
        measure = Measure.objects.get(pk=measure_id)
    except Measure.DoesNotExist:
        raise Http404
    #p = get_object_or_404(Measure, pk=poll_id)
    return render_to_response('polls/detail.html', {'measure': measure})

#TODO: keep the last values for each measure in the separate record!!!
#TODO: validate data
#TODO: store input in logs!
def handle_value(request):
    name = request.GET['name']
    value = float(request.GET['value'])
    unitOfMeasure = request.GET['unit']
    year = int(request.GET['year'])
    month = int(request.GET['month'])
    day = int(request.GET['day'])
    hour = int(request.GET['hour'])
    min = int(request.GET['min'])
    sec = int(request.GET['sec'])    
    measureDate = datetime(year,  month,  day,  hour,  min,  sec)
    measure =  Measure(Name = name,  
                       Value = value, 
                       MeasureDate = measureDate, 
                       UnitOfMeasure = unitOfMeasure)
    measure.save()
    return render_to_response('polls/insert.html', {'measure':measure})
