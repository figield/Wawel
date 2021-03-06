from polls.models import Measure
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from customclasses import Cost
from configuration import *

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

def calculate_thermal():
    ydict = {}
    mdict = {}
    All = Measure.objects.filter(Name = 'thermal').order_by('MeasureDate')
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
                               round(YUsage * GJ, 3),
                               0))
    m_keys = mdict.keys()
    m_keys.sort()
    Monthscosts = []
    for m_key in m_keys:
        (MMin, MMax) = mdict.get(m_key)
        MUsage = MMax - MMin
        Monthscosts.append(Cost(m_key,
                                round(MUsage * GJ, 3),
                                0))
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

def calculate_month_thermal(Year, Month):
    MThermalMin = 0
    MThermalMax = 0
    Thermals = Measure.objects.filter( UnitOfMeasure = "GJ", 
                                    Name = "thermal",  
                                    MeasureDate__year = Year,
                                    MeasureDate__month = Month
                                    ).order_by('MeasureDate')
    for measure in Thermals:
        if MThermalMax == 0:
            MThermalMin = measure.Value
            MThermalMax = measure.Value
        else:
            if MThermalMin > measure.Value:
                MThermalMin = measure.Value
            if MThermalMax < measure.Value:
                MThermalMax = measure.Value

    return MThermalMax - MThermalMin


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
                DElecMax = measure.Value

    MUsage = DElecMax - DElecMin
    DayCost = round(MUsage * CostPerkWh, 2)
    return (DayCost, MUsage)

def calculate_cost_for_prev_day(year, month, day):
    prevDate = datetime(year, month, day) + relativedelta(days=-1)
    return calculate_day_cost(prevDate.year, prevDate.month, prevDate.day)

def get_next_day(year, month, day, daydiff, name):
    if validate_date_ymd(year, month, day):
        nextDate = datetime(int(year), int(month), int(day)) + relativedelta(days=daydiff)
        nextMeasures = Measure.objects.filter(
            Name = name,
            MeasureDate__year = nextDate.year, 
            MeasureDate__month = nextDate.month,
            MeasureDate__day = nextDate.day)
        if len(nextMeasures) > 0:
            return nextDate.strftime("%Y/%m/%d")
        else:
            return False
    else:
        return False

def get_days_of_the_month(year, month):
    days = []
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        Date = measure.MeasureDate.strftime("%Y/%m/%d")
        if Date not in days:
            days.append(Date)
    return days

def get_next_month(year, month, monthdiff, name):
    if validate_date_ym(year, month):
        nextDate = datetime(int(year), int(month), 1) + relativedelta(months=monthdiff)
        nextMeasures = Measure.objects.filter(
            Name = name,
            MeasureDate__year = nextDate.year, 
            MeasureDate__month = nextDate.month)
        if len(nextMeasures) > 0:
            return nextDate.strftime("%Y/%m")
        else:
            return False
    else:
        return False

def validate_year(year):
    try:
        intyear = int(year)
        if intyear > 2010 and intyear < 2034:
            return True
        else:
            return False
    except: 
        return False

def validate_month(month):
    try:
        intmonth = int(month)
        if intmonth > 0 and intmonth < 13:
            return True
        else:
            return False
    except: 
        return False

def validate_date(year, month, day):
    try:
        datetime(int(year), int(month), int(day))
        return True
    except: 
        return False

def validate_date_ymd(y,m,d):
    return validate_date(y, m, d)

def validate_date_ym(y,m):
    return validate_year(y) and validate_month(m)
