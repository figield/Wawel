from polls.models import Measure, LastMeasure, MeasureMonth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext
from datetime import date, datetime
from graphs import * 
from calculation import * 
from configuration import * 
from customclasses import *
import random

# For Ajax requests in the include.html
def update_temp(request, id):

    if id == 'in':
        Tid = IN
    else:
        Tid = OUT

    Temps = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                        Name = Tid,  
                                        MeasureDate__year = date.today().year
                                        ).order_by('MeasureDate')
    if len(Temps) == 0:
        if Tid == IN:
            return render_to_response('polls/temp_in.html', {'in':0})
        else:
            return render_to_response('polls/temp_out.html', {'out':0})
    else:
        Temp = Temps[len(Temps) -1 ].Value 
        R = random.randint(-4, 4) * 0.1
        if Tid == IN:
            return render_to_response('polls/temp_in.html', {'in':Temp + R})
        else:
            return render_to_response('polls/temp_out.html', {'out':Temp + R})

# For Ajax requests in the index.html
def update_temp2(request, id):
    if id == 'in':
        Tid = IN
    else:
        Tid = OUT
    Temps = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                        Name = Tid,  
                                        MeasureDate__year = date.today().year
                                        ).order_by('MeasureDate')
    if len(Temps) == 0:
        if Tid == IN:
            return render_to_response('polls/temp.html', {'in':0})
        else:
            return render_to_response('polls/temp.html', {'out':0})
    else:
        Temp = Temps[len(Temps) -1 ].Value 
        R = random.randint(-4, 4) * 0.1
        if Tid == IN:
            return render_to_response('polls/temp.html', {'in':Temp + R})
        else:
            return render_to_response('polls/temp.html', {'out':Temp + R})

def index(request):

    year = date.today().year
    month = date.today().month
    day = date.today().day

    Outs = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                       Name = OUT,  
                                       MeasureDate__year = year
                                       ).order_by('MeasureDate')
    if len(Outs) == 0:
        Out = 0
    else:
        Out = Outs[len(Outs) -1 ].Value        

    Ins = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                      Name = IN,  
                                      MeasureDate__year = year
                                      ).order_by('MeasureDate')
    if len(Ins) == 0:
        In = 0
    else:
        In = Ins[len(Ins) -1 ].Value
    
    (DayCost, DUsage) = calculate_day_cost(year, month, day)
    (MonthCost, MonthElecUsage) = calculate_month_cost(year, month)
    MonthThermalUsage = calculate_month_thermal(year, month)

    if MonthElecUsage == 0:
        cop = 0
    else:
        cop = round(MonthThermalUsage * GJ / MonthElecUsage, 3)

    ThermalKWh = round(MonthThermalUsage * GJ, 3)

    return render_to_response('polls/index.html',
                              {'out':Out,  
                               'in':In,  
                               'elec':MonthElecUsage,  
                               'thermalkwh':ThermalKWh, 
                               'cop':cop,
                               'day_cost':DayCost,
                               'month_cost':MonthCost
                               })

def include(request):

    year = date.today().year
    month = date.today().month
    day = date.today().day

    Outs = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                       Name = OUT,  
                                       MeasureDate__year = year
                                       ).order_by('MeasureDate')
    if len(Outs) == 0:
        Out = 0
    else:
        Out = Outs[len(Outs) -1 ].Value        

    Ins = LastMeasure.objects.filter( UnitOfMeasure = "C", 
                                      Name = IN,  
                                      MeasureDate__year = year
                                      ).order_by('MeasureDate')
    if len(Ins) == 0:
        In = 0
    else:
        In = Ins[len(Ins) -1 ].Value

    (DayCost, DUsage) = calculate_day_cost(year, month, day)
    (MonthCost, MUsage) = calculate_month_cost(year, month)

    (Yearscosts, Monthscosts) = calculate_costs()

    return render_to_response('polls/include.html',
                              {'out':Out,  
                               'in':In,  
                               'day_cost':DayCost,
                               'month_cost':MonthCost,
                               'yearscosts':Yearscosts,
                               'monthscosts':Monthscosts
                               })

def photos(request):
    return render_to_response('polls/photos.html', {})

def movie1(request):
    return render_to_response('polls/movie1.html', {})

def movie2(request):
    return render_to_response('polls/movie2.html', {})

def daytemp(request, year, month, day):
    if not validate_date_ymd(year, month, day):
        return HttpResponseRedirect('/') 

    (x_labels, dataDict) = generate_data_for_daychart_temp_in_out(year,month, day)

    TempsIn = dataDict.get(IN)
    if TempsIn == None:
        TempsIn = []

    TempsOut = dataDict.get(OUT)
    if TempsOut == None:
        TempsOut = []

    data = []
    for (x_label, TempOut, TempIn) in zip(x_labels, TempsOut, TempsIn):
        data.append([x_label, TempOut, TempIn])

    nextDate = get_next_day(year, month, day, 1, IN)
    if nextDate == False:
        days = get_days_of_the_month(year, month)
        currentDate = datetime(int(year), int(month), int(day)).strftime("%Y/%m/%d")
        for idate in days:
            if currentDate < idate:
                nextDate = idate
                break

    prevDate = get_next_day(year, month, day, -1, IN)
    if prevDate == False:
        days = get_days_of_the_month(year, month)        
        currentDate = datetime(int(year), int(month), int(day)).strftime("%Y/%m/%d")
        days.reverse()
        for idate in days:
            if currentDate > idate:
                prevDate = idate
                break

    return render_to_response('polls/daytemp.html', 
                              {'year':year,
                               'month':month,
                               'day':day,
                               'data':data,
                               'nextdate':nextDate,
                               'prevdate':prevDate
                               })

def monthtemp(request, year, month):
    if not validate_date_ym(year, month):
        return HttpResponseRedirect('/') 

    (x_labels, dataDict) = generate_data_for_monthchart_temp_in_out(year,month)

    TempsIn = dataDict.get(IN)
    if TempsIn == None:
        TempsIn = []

    TempsOut = dataDict.get(OUT)
    if TempsOut == None:
        TempsOut = []

    data = []
    for (x_label, TempOut, TempIn) in zip(x_labels, TempsOut, TempsIn):
        data.append([x_label, TempOut, TempIn])

    days = get_days_of_the_month(year, month)

    nextDate = get_next_month(year, month, 1, IN)
    prevDate = get_next_month(year, month, -1, IN)

    return render_to_response('polls/monthtemp.html', 
                              {'year':year,  
                               'month':month,
                               'days':days,
                               'data':data,
                               'nextdate':nextDate,
                               'prevdate':prevDate},
                              context_instance=RequestContext(request))

def dayenergy(request, year, month, day):
    if not validate_date_ymd(year, month, day):
        return HttpResponseRedirect('/') 

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

    nextDate = get_next_day(year, month, day, 1, 'elec')
    if nextDate == False:
        days = get_days_of_the_month(year, month)
        currentDate = datetime(int(year), int(month), int(day)).strftime("%Y/%m/%d")
        for idate in days:
            if currentDate < idate:
                nextDate = idate
                break

    prevDate = get_next_day(year, month, day, -1, 'elec')
    if prevDate == False:
        days = get_days_of_the_month(year, month)
        currentDate = datetime(int(year), int(month), int(day)).strftime("%Y/%m/%d")
        days.reverse()
        for idate in days:
            if currentDate > idate:
                prevDate = idate
                break

    return render_to_response('polls/dayenergy.html', 
                              {'year':year,
                               'month':month,
                               'day':day,
                               'data':data,
                               'nextdate':nextDate,
                               'prevdate':prevDate})

def monthenergy(request, year, month):
    if not validate_date_ym(year, month):
        return HttpResponseRedirect('/') 

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

    days = get_days_of_the_month(year, month)
    
    nextDate = get_next_month(year, month, 1, 'elec')
    prevDate = get_next_month(year, month, -1, 'elec')

    return render_to_response('polls/monthenergy.html', 
                              {'year':year,  
                               'month':month,
                               'days':days,
                               'data':data,
                               'nextdate':nextDate,
                               'prevdate':prevDate},
                              context_instance=RequestContext(request))

def yearenergy(request, year):
    if not validate_year(year):
        return HttpResponseRedirect('/') 

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
                               'year':year,
                               'data':data},
                              context_instance=RequestContext(request))

def yeartemp(request, year):
    if not validate_year(year):
        return HttpResponseRedirect('/') 

    months = MeasureMonth.objects.all()
    (x_labels, dataDict) = generate_data_for_yearchart_temp_in_out(year)

    TempsIn = dataDict.get(IN)
    if TempsIn == None:
        TempsIn = []

    TempsOut = dataDict.get(OUT)
    if TempsOut == None:
        TempsOut = []

    data = []
    for (x_label, TempOut, TempIn) in zip(x_labels, TempsOut, TempsIn):
        data.append([x_label, TempOut, TempIn])
    return render_to_response('polls/yeartemp.html', 
                              {'months':months, 
                               'year':year,
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
    lastMeasures = LastMeasure.objects.filter(UnitOfMeasure = unitOfMeasure, 
                                              Name = name)
    fixedvalue = 0
    if len(lastMeasures) > 0:
        fixedvalue = lastMeasures[0].Value
        lastMeasures[0].delete()

    if value <= 0 and (name == "thermal" or name == "elec"):
        value = fixedvalue 

    measure = Measure(Name = name,  
                      Value = value, 
                      MeasureDate = measureDate, 
                      UnitOfMeasure = unitOfMeasure)
    if value < -100:
        return render_to_response('polls/insert.html', {'measure':measure})

    measure.save()
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
    (YearsCosts, MonthsCosts) = calculate_costs()
    (YearsThermal, MonthsThermal) = calculate_thermal()
    YearCalc = []
    for (YearCosts, YearThermal) in zip(YearsCosts, YearsThermal):
        YearCalc.append(Usage(YearCosts.period,
                              YearCosts.usage,
                              YearCosts.cost,
                              YearThermal.usage))
    MonthCalc = []
    for (MonthCosts, MonthThermal) in zip(MonthsCosts, MonthsThermal):
        MonthCalc.append(Usage(MonthCosts.period,
                               MonthCosts.usage,
                               MonthCosts.cost,
                               MonthThermal.usage))

    return render_to_response('polls/costs.html', 
                              {'yearscosts':YearCalc,
                               'monthscosts':MonthCalc})

def contact(request):            
    return render_to_response('polls/contact.html', {})

def heating(request):            
    return render_to_response('polls/heating.html', {})

def anyrequest(request, fake):            
    return HttpResponseRedirect('/') 
