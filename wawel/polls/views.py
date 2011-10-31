from polls.models import Measure, LastMeasure, MeasureMonth
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.http import Http404
from django.template import RequestContext
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from customclasses import Cost
from viewsgraphs import * 
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
    
    Elecs = LastMeasure.objects.filter( UnitOfMeasure = "kWh", 
                                        Name = "elec",  
                                        MeasureDate__year = year
                                        ).order_by('MeasureDate')
    if len(Elecs) == 0:
        Elec = 0
    else:
        Elec = Elecs[len(Elecs) -1 ].Value

    Thermals = LastMeasure.objects.filter( UnitOfMeasure = "GJ", 
                                           Name = "thermal",  
                                           MeasureDate__year = year
                                           ).order_by('MeasureDate')
    if len(Thermals) == 0:
        ThermalGJ = 0
    else:
        ThermalGJ = Thermals[len(Thermals) -1 ].Value
    ThermalKWh = round(ThermalGJ * GJ, 2) 
    if Elec == 0:
        cop = 0
    else:
        cop = round(ThermalKWh / Elec, 3)

    (DayCost, DUsage) = calculate_cost_for_prev_day(year, month, day)
    if DayCost == 0:
        DayCost = 5.0 # Estimated cost

    (MonthCost, MUsage) = calculate_cost_for_prev_month(year, month)
    if MonthCost == 0:
        MonthCost = 150.0 # Estimated cost

    return render_to_response('polls/index.html', # TODO: add comments
                              {'out':Out,  
                               'in':In,  
                               'elec':Elec,  
                               'thermalgj':ThermalGJ,  
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

    (DayCost, DUsage) = calculate_cost_for_prev_day(year, month, day)
    if DayCost == 0:
        DayCost = 5.0 # Estimated cost

    (MonthCost, MUsage) = calculate_cost_for_prev_month(year, month)
    if MonthCost == 0:
        MonthCost = 150.0 # Estimated cost

    (Yearscosts, Monthscosts) = calculate_costs()

    return render_to_response('polls/include.html', # TODO: fix template
                              {'out':Out,  
                               'in':In,  
                               'day_cost':DayCost,
                               'month_cost':MonthCost,
                               'yearscosts':Yearscosts,
                               'monthscosts':Monthscosts
                               })

def photos(request):
    return render_to_response('polls/photos.html', {})

def daytemp(request, year, month, day):
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
    prevDate = get_next_day(year, month, day, -1, IN)

    return render_to_response('polls/daytemp.html', 
                              {'year':year,
                               'month':month,
                               'day':day,
                               'data':data,
                               'nextdate':nextDate,
                               'prevdate':prevDate
                               })

# TODO: move to file with lib functions

def get_next_day(year, month, day, daydiff, name):
    # TODO: validate!
    nextDate = datetime(int(year), int(month), int(day)) + relativedelta(days=daydiff)
    nextYear = nextDate.year
    nextMonth = nextDate.month
    nextDay = nextDate.day
    nextMeasures = Measure.objects.filter(
        Name = name,
        MeasureDate__year = nextYear, 
        MeasureDate__month = nextMonth,
        MeasureDate__day = nextDay)
    if len(nextMeasures) > 0:
        return str(nextYear)+ "/" + str(nextMonth) + "/" + str(nextDay)
    else:
        return False

def get_next_month(year, month, monthdiff, name):
    # TODO: validate!
    nextDate = datetime(int(year), int(month), 1) + relativedelta(months=monthdiff)
    nextYear = nextDate.year
    nextMonth = nextDate.month
    nextMeasures = Measure.objects.filter(
        Name = name,
        MeasureDate__year = nextYear, 
        MeasureDate__month = nextMonth)
    if len(nextMeasures) > 0:
        return str(nextYear)+ "/" + str(nextMonth)
    else:
        return False
    
def monthtemp(request, year, month):
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

    days = []
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        Date = measure.MeasureDate.strftime("%Y/%m/%d")
        if Date not in days:
            days.append(Date)

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

    nextDate = get_next_day(year, month, day, 1, 'elec')
    prevDate = get_next_day(year, month, day, -1, 'elec')

    return render_to_response('polls/dayenergy.html', 
                              {'year':year,
                               'month':month,
                               'day':day,
                               'data':data,
                               'nextdate':nextDate,
                               'prevdate':prevDate})

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
    # TODO: validate!
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
    (Yearscosts, Monthscosts) = calculate_costs()
    return render_to_response('polls/costs.html', 
                              {'yearscosts':Yearscosts,
                               'monthscosts':Monthscosts})

def calculate_costs():
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
    return (Yearscosts, Monthscosts)

def calculate_month_cost(Year, Month):
    MElecMin = 0
    MElecMax = 0
    Elecs = Measure.objects.filter( UnitOfMeasure = "kWh", 
                                    Name = "elec",  
                                    MeasureDate__year = Year,
                                    MeasureDate__month = Month
                                    ).order_by('MeasureDate')
    for measure in Elecs:
        if MElecMax == 0:
            MElecMin = measure.Value
            MElecMax = measure.Value
        else:
            if MElecMin > measure.Value:
                MElecMin = measure.Value
            if MElecMax < measure.Value:
                MElecMax = measure.Value

    MUsage = MElecMax - MElecMin
    MonthCost = round(MUsage * CostPerkWh, 2)
    return (MonthCost, MUsage)

def calculate_cost_for_prev_month(year, month):
    prevDate = datetime(year, month, 1) + relativedelta(months=-1)
    prevYear = prevDate.year
    prevMonth = prevDate.month
    return calculate_month_cost(prevYear, prevMonth)

def calculate_day_cost(Year, Month, Day):
    DElecMin = 0
    DElecMax = 0
    Elecs = Measure.objects.filter( UnitOfMeasure = "kWh", 
                                    Name = "elec",  
                                    MeasureDate__year = Year,
                                    MeasureDate__month = Month,
                                    MeasureDate__day = Day
                                    ).order_by('MeasureDate')
    for measure in Elecs:
        if DElecMax == 0:
            DElecMin = measure.Value
            DElecMax = measure.Value
        else:
            if DElecMin > measure.Value:
                DElecMin = measure.Value
            if DElecMax < measure.Value:
                # TODO: fix Max value - take the Min from next day
                DElecMax = measure.Value

    MUsage = DElecMax - DElecMin
    DayCost = round(MUsage * CostPerkWh, 2)
    return (DayCost, MUsage)

def calculate_cost_for_prev_day(year, month, day):
    prevDate = datetime(year, month, day) + relativedelta(days=-1)
    prevYear = prevDate.year
    prevMonth = prevDate.month
    prevDay = prevDate.day
    return calculate_day_cost(prevYear, prevMonth, prevDay)

def contact(request):            
    return render_to_response('polls/contact.html', {})

def heating(request):            
    return render_to_response('polls/heating.html', {})

def anyrequest(request, fake):            
    return HttpResponseRedirect('/') 
