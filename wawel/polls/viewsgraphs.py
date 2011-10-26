from polls.models import Measure
from datetime import date, datetime
from django.db.models import Q

IN = 'WEW'
OUT = 'ZEW'

def generate_data_for_yearchart_temp_in_out(year):
    dict = {}
    for measure in Measure.objects.filter(Q(Name=OUT) | Q(Name=IN),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        month = measure.MeasureDate.strftime("%Y/%m")
        DN = dict.get(month)
        if DN == None:
            dict[month] = {measure.Name:(measure.Value, 1)}
        else:
            VN = DN.get(measure.Name)
            if VN == None:
                DN[measure.Name] = (measure.Value, 1)
            else:
                (V, N) = VN
                DN[measure.Name] = (V + measure.Value, N + 1)
            dict[month] = DN
    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    for month in x_labels:
        DN = dict.get(month)
        for name in DN.keys():
            (V, N) = DN.get(name)
            if data.get(name) == None:
                data[name] = []
            data[name].append(int(V/N))
    return (x_labels, data)

def generate_data_for_yearbarchart_energy(year):
    dict = {}
    for measure in Measure.objects.filter(Name = 'elec',
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        month = measure.MeasureDate.strftime("%Y/%m")
        Tuple = dict.get(month)
        if Tuple == None:
            dict[month] = (measure.Value, measure.Value)
        else:
            (Min, Max) = Tuple
            if Min > measure.Value:
                Min = measure.Value
            if Max < measure.Value:
                Max = measure.Value            
            dict[month] = (Min, Max)
            
    dict2 = {}
    for measure in Measure.objects.filter(Name = 'thermal',
                                          MeasureDate__year = 
                                          int(year)).order_by('MeasureDate'):
        month = measure.MeasureDate.strftime("%Y/%m")
        Tuple2 = dict2.get(month)
        if Tuple2 == None:
            dict2[month] = (measure.Value, measure.Value)
        else:
            (Min, Max) = Tuple2
            if Min > measure.Value:
                Min = measure.Value
            if Max < measure.Value:
                Max = measure.Value            
            dict2[month] = (Min, Max)

    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    name = 'elec'
    name2 = 'thermal'
    data[name] = []
    data[name2] = []
    for month in x_labels:
        (Min, Max) = dict.get(month)
        (Min2, Max2) = dict2.get(month)
        data[name].append(round(Max - Min, 4))
        data[name2].append(round((Max2 - Min2) * 277.77777777778, 4))
    return (x_labels, data)

def generate_data_for_monthchart_temp_in_out(year, month):
    dict = {}
    for measure in Measure.objects.filter(Q(Name=OUT) | Q(Name=IN), 
                                          MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        time = measure.MeasureDate.strftime("%d")
        DN = dict.get(time)
        if DN == None:
            dict[time] = {measure.Name:(measure.Value, 1)}
        else:
            VN = DN.get(measure.Name)
            if VN == None:
                DN[measure.Name] = (measure.Value, 1)
            else:
                (V, N) = VN
                DN[measure.Name] = (V + measure.Value, N + 1)
            dict[time] = DN
    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    for time in x_labels:
        DN = dict.get(time)
        for name in DN.keys():
            (V, N) = DN.get(name)
            if data.get(name) == None:
                data[name] = []
            data[name].append(int(V/N))
    return (x_labels, data)

def generate_data_for_monthbarchart_energy(year, month):
    dict = {}
    for measure in Measure.objects.filter(Name = 'elec',
                                          UnitOfMeasure = "kWh",
                                          MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        day = measure.MeasureDate.strftime("%d")
        Tuple = dict.get(day)
        if Tuple == None:
            dict[day] = (measure.Value, measure.Value)
        else:
            (Min, Max) = Tuple
            if Min > measure.Value:
                Min = measure.Value
            if Max < measure.Value:
                Max = measure.Value            
            dict[day] = (Min, Max)
            
    dict2 = {}
    for measure in Measure.objects.filter(Name = 'thermal',
                                          UnitOfMeasure = "GJ",
                                          MeasureDate__month = int(month),
                                          MeasureDate__year = int(year)).order_by('MeasureDate'):
        day = measure.MeasureDate.strftime("%d")
        Tuple2 = dict2.get(day)
        if Tuple2 == None:
            dict2[day] = (measure.Value, measure.Value)
        else:
            (Min, Max) = Tuple2
            if Min > measure.Value:
                Min = measure.Value
            if Max < measure.Value:
                Max = measure.Value            
            dict2[day] = (Min, Max)

    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    name = 'elec'
    name2 = 'thermal'
    if data.get(name) == None:
        data[name] = []
    if data.get(name2) == None:
        data[name2] = []
    for day in x_labels:
        (Min, Max) = dict.get(day)
        (Min2, Max2) = dict2.get(day)
        data[name].append(round(Max - Min, 4))
        data[name2].append(round((Max2 - Min2) * 277.77777777778, 4))
    return (x_labels, data)


def generate_data_for_daychart_temp_in_out(year, month, day):
    data = {}
    x_labels = []
    for measure in Measure.objects.filter(UnitOfMeasure = "C", 
                                          MeasureDate__month = int(month),
                                          MeasureDate__year = int(year), 
                                          MeasureDate__day = int(day)).order_by('MeasureDate'):
        Date = measure.MeasureDate.strftime("%H:%M")
        if data.get(measure.Name)==None:
            data[measure.Name] = [measure.Value]            
            if Date not in x_labels:
                x_labels  = [Date]
        else:
            data[measure.Name].append(measure.Value)
            if Date not in x_labels:
                x_labels.append(Date)    
    return (x_labels, data)

def generate_data_for_daybarchart_energy(year, month, day):
    dict = {}
    name = 'elec'
    name2 = 'thermal'
    for measure in Measure.objects.filter(Name = name, 
                                          MeasureDate__month = int(month),
                                          MeasureDate__year = int(year), 
                                          MeasureDate__day = int(day)).order_by('MeasureDate'):
        Time = measure.MeasureDate.strftime("%H:%M")
        dict[Time] = measure.Value
            
    dict2 = {}
    for measure in Measure.objects.filter(Name = name2, 
                                          MeasureDate__month = int(month),
                                          MeasureDate__year = int(year), 
                                          MeasureDate__day = int(day)).order_by('MeasureDate'):
        Time = measure.MeasureDate.strftime("%H:%M")
        dict2[Time] = measure.Value

    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    data[name] = []
    data[name2] = []
    PrevVal = 0
    PrevVal2 = 0
    for Time in x_labels:
        PrevVal = dict.get(Time)
        PrevVal2 = dict2.get(Time) * 277.77777777778
        break
    for Time in x_labels:
        Val = dict.get(Time)
        Val2 = dict2.get(Time) * 277.77777777778
        data[name].append(round(Val - PrevVal, 4))
        data[name2].append(round(Val2 - PrevVal2, 4))
        PrevVal = Val
        PrevVal2 = Val2
    return (x_labels, data)
