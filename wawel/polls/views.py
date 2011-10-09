from polls.models import Measure, LastMeasure, MeasureMonth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext
from datetime import date, datetime
from customclasses import Cost
from viewsgraphs import generate_data_for_yearchart_temp_in_out
from viewsgraphs import generate_data_for_monthchart_temp_in_out
from viewsgraphs import generate_data_for_daychart_temp_in_out
from viewsgraphs import generate_data_for_yearbarchart_energy
from viewsgraphs import generate_data_for_monthbarchart_energy
from viewsgraphs import generate_data_for_daybarchart_energy
import random

# For Ajax requests
def update_temp(request, id):
    Temps = LastMeasure.objects.filter( UnitOfMeasure = "C", 
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
    Outs = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                       Name = "out",  
                                       MeasureDate__year = date.today().year
                                       ).order_by('MeasureDate')
    if len(Outs) == 0:
        Out = 0
    else:
        Out = Outs[len(Outs) -1 ].Value        

    Ins = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                      Name = "in",  
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

    Thermals = LastMeasure.objects.filter( UnitOfMeasure = "GJ", 
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
        cop = round(ThermalKWh / Elec, 3)

    # TODO: calculate day's costs of electricity usage
    day_cost = 5.0
    # TODO: calculate month's costs
    month_cost = 30 * 5.0

    return render_to_response('polls/index.html', 
                              {'out':Out,  
                               'in':In,  
                               'elec':Elec,  
                               'thermalgj':ThermalGJ,  
                               'thermalkwh':ThermalKWh, 
                               'cop':cop,
                               'day_cost':day_cost,
                               'month_cost':month_cost
                               })

def photos(request):
    return render_to_response('polls/photos.html', {})

def daytemp(request, year,  month, day):
    (x_labels, dataDict) = generate_data_for_daychart_temp_in_out(year,month, day)

    TempsIn = dataDict.get('in')
    if TempsIn == None:
        TempsIn = []

    TempsOut = dataDict.get('out')
    if TempsOut == None:
        TempsOut = []

    data = []
    for (x_label, TempOut, TempIn) in zip(x_labels, TempsOut, TempsIn):
        data.append([x_label, TempOut, TempIn])

    return render_to_response('polls/daytemp.html', 
                              {'year':year,
                               'month':month,
                               'day':day,
                               'data':data})

def monthtemp(request, year, month):
    (x_labels, dataDict) = generate_data_for_monthchart_temp_in_out(year,month)

    TempsIn = dataDict.get('in')
    if TempsIn == None:
        TempsIn = []

    TempsOut = dataDict.get('out')
    if TempsOut == None:
        TempsOut = []

    data = []
    for (x_label, TempOut, TempIn) in zip(x_labels, TempsOut, TempsIn):
        data.append([x_label, TempOut, TempIn])

    days = []
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        Date = measure.MeasureDate.strftime("%Y/%m/%d")
        if Date not in days:
            days.append(Date)

    return render_to_response('polls/monthtemp.html', 
                              {'year':year,  
                               'month':month,
                               'days':days,
                               'data':data},
                              context_instance=RequestContext(request))

def dayenergy(request, year,  month, day):
    (x_labels, dataDict) = generate_data_for_daybarchart_energy(year,month, day)
    Elecs = dataDict.get('elec')
    if Elecs == None:
        Elecs = []

    Thermals = dataDict.get('thermal')
    if Thermals == None:
        Thermals = []

    data = []
    for (x_label, Elec, Thermal) in zip(x_labels, Elecs, Thermals):
        data.append([x_label, Elec, Thermal])
    return render_to_response('polls/dayenergy.html', 
                              {'year':year,
                               'month':month,
                               'day':day,
                               'data':data})

def monthenergy(request, year, month):
    (x_labels, dataDict) = generate_data_for_monthbarchart_energy(year, month)

    Elecs = dataDict.get('elec')
    if Elecs == None:
        Elecs = []

    Thermals = dataDict.get('thermal')
    if Thermals == None:
        Thermals = []

    data = []
    for (x_label, Elec, Thermal) in zip(x_labels, Elecs, Thermals):
        data.append([x_label, Elec, Thermal])

    days = []
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        Date = measure.MeasureDate.strftime("%Y/%m/%d")
        if Date not in days:
            days.append(Date)

    return render_to_response('polls/monthenergy.html', 
                              {'year':year,  
                               'month':month,
                               'days':days,
                               'data':data},
                              context_instance=RequestContext(request))

def yearenergy(request, year):
    months = MeasureMonth.objects.all()
    (x_labels, dataDict) = generate_data_for_yearbarchart_energy(year)

    Elecs = dataDict.get('elec')
    if Elecs == None:
        Elecs = []

    Thermals = dataDict.get('thermal')
    if Thermals == None:
        Thermals = []

    data = []
    for (x_label, Elec, Thermal) in zip(x_labels, Elecs, Thermals):
        data.append([x_label, Elec, Thermal])
    return render_to_response('polls/yearenergy.html', 
                              {'months':months, 
                               'data':data},
                              context_instance=RequestContext(request))

def yeartemp(request, year):
    months = MeasureMonth.objects.all()
    (x_labels, dataDict) = generate_data_for_yearchart_temp_in_out(year)

    TempsIn = dataDict.get('in')
    if TempsIn == None:
        TempsIn = []

    TempsOut = dataDict.get('out')
    if TempsOut == None:
        TempsOut = []

    data = []
    for (x_label, TempOut, TempIn) in zip(x_labels, TempsOut, TempsIn):
        data.append([x_label, TempOut, TempIn])
    return render_to_response('polls/yeartemp.html', 
                              {'months':months, 
                               'data':data},
                              context_instance=RequestContext(request))

def selectmonth(request):
    Month = "2011/12"
    if request.method == 'POST':
        Month = request.POST['selectmonth']
    return HttpResponseRedirect('/monthtemp/'+ Month +'/') 

def selectmonth_energy(request):
    Month = "2011/12"
    if request.method == 'POST':
        Month = request.POST['selectmonth']
    return HttpResponseRedirect('/monthenergy/'+ Month +'/') 

def selectday(request):
    Day = "2011/12/01"
    if request.method == 'POST':
        Day = request.POST['selectday']
    return HttpResponseRedirect('/daytemp/'+ Day +'/') 

def selectday_energy(request):
    Day = "2011/12/01"
    if request.method == 'POST':
        Day = request.POST['selectday']
    return HttpResponseRedirect('/dayenergy/'+ Day +'/') 

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
    sec = 0

    measureDate = datetime(year,  month,  day,  hour,  min,  sec)

    if name == "temp_3":
        name = "in"
    elif name == "temp_2":
        name = "out"

    measure = Measure(Name = name,  
                      Value = value, 
                      MeasureDate = measureDate, 
                      UnitOfMeasure = unitOfMeasure)

    if value < -100:
        return render_to_response('polls/insert.html', {'measure':measure})

    measure.save()

    lastMeasures = LastMeasure.objects.filter(UnitOfMeasure = unitOfMeasure, 
                                             Name = name)
    if len(lastMeasures) > 0:
        lastMeasures[0].delete()

    lastMeasure = LastMeasure(Name = name,  
                              Value = value, 
                              MeasureDate = measureDate, 
                              UnitOfMeasure = unitOfMeasure)
    lastMeasure.save()

    date = measure.MeasureDate.strftime("%Y/%m")
    measureMonths = MeasureMonth.objects.filter(Month = date) 
    if len(measureMonths) == 0:
        measureMonth = MeasureMonth(Month = date)
        measureMonth.save()

    return render_to_response('polls/insert.html', {'measure':measure})

def costs(request):
    ydict = {}
    mdict = {}
    All = Measure.objects.filter(Name = 'elec').order_by('MeasureDate')
    for measure in All:

        year = measure.MeasureDate.strftime("%Y")
        YTuple = ydict.get(year)
        if YTuple == None:
            ydict[year] = (measure.Value, measure.Value)
        else:
            (Min, Max) = YTuple
            if Min > measure.Value:
                Min = measure.Value
            if Max < measure.Value:
                Max = measure.Value            
            ydict[year] = (Min, Max)

        month = measure.MeasureDate.strftime("%Y/%m")
        MTuple = mdict.get(month)
        if MTuple == None:
            mdict[month] = (measure.Value, measure.Value)
        else:
            (MMin, MMax) = MTuple
            if MMin > measure.Value:
                MMin = measure.Value
            if MMax < measure.Value:
                MMax = measure.Value            
            mdict[month] = (MMin, MMax)
    
    CostPerkWh = 0.55
    y_keys = ydict.keys()
    y_keys.sort()
    Yearscosts = []
    for y_key in y_keys:
        (YMin, YMax) = ydict.get(y_key)
        YUsage = YMax - YMin
        Yearscosts.append(Cost(y_key,
                               YUsage,
                               round(YUsage * CostPerkWh, 2)))
    m_keys = mdict.keys()
    m_keys.sort()
    Monthscosts = []
    for m_key in m_keys:
        (MMin, MMax) = mdict.get(m_key)
        MUsage = MMax - MMin
        Monthscosts.append(Cost(m_key,
                                MUsage,
                                round(MUsage * CostPerkWh, 2)))

    return render_to_response('polls/costs.html', 
                              {'yearscosts':Yearscosts,
                               'monthscosts':Monthscosts})

def contact(request):            
    return render_to_response('polls/contact.html', {})
