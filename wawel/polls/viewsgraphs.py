from polls.models import Measure
from django.http import HttpResponse
from datetime import date, datetime
import math, random
import cairo
import cairoplot

def yearchart(request,  name):
    dict = {}
    unit = ""
    for measure in Measure.objects.filter(Name = name):
        month = measure.MeasureDate.strftime("%Y/%m")
        VN = dict.get(month)
        if VN == None:
            unit = measure.UnitOfMeasure
            dict[month] = (measure.Value, 1)
        else:
            (V, N) = VN
            dict[month] = ( V + measure.Value, N + 1)
    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    data[name] = []
    for month in x_labels:
        (V, N) = dict.get(month)
        data[name].append(round(V/N,  1))
    return draw_graph(data,  x_labels,  unit)

def yearchart_temp(request):
    dict = {}
    for measure in Measure.objects.filter(UnitOfMeasure = "C"):
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
    return draw_graph(data,  x_labels,  "Degrees Celsius")

def monthchart(request, name, year, month):
    dict = {}
    unit = ""
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year),
                                          Name = name).order_by('MeasureDate'):
        day = measure.MeasureDate.strftime("%d")
        VN = dict.get(day)
        if VN == None:
            unit = measure.UnitOfMeasure
            dict[day] = (measure.Value, 1)
        else:
            (V, N) = VN
            dict[day] = ( V + measure.Value, N + 1)
    data = {}
    x_labels = dict.keys()
    x_labels.sort()
    data[name] = []
    for day in x_labels:
        (V, N) = dict.get(day)
        data[name].append(int(V/N))
    return draw_graph(data,  x_labels,  unit)

def monthchart_temp(request, year, month):
    dict = {}
    for measure in Measure.objects.filter(UnitOfMeasure = "C", 
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
    return draw_graph(data,  x_labels,  "Degrees Celsius")

def month_barchart(request, year, month):
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
    data = []
    for day in x_labels:
        (Min, Max) = dict.get(day)
        (Min2, Max2) = dict2.get(day)
        data.append([int(Max2 - Min2),  int(Max - Min)])
    y_labels = None
    return draw_bar_graph(data, x_labels, y_labels)

def daychart(request, name, year, month, day):
    data = {}
    x_labels = []
    unit = ""
    for measure in Measure.objects.filter(MeasureDate__month = int(month),
                                          MeasureDate__year = int(year), 
                                          MeasureDate__day = int(day),
                                          Name = name).order_by('MeasureDate'):
        if data.get(name)==None:
            data[name] = [measure.Value]
            x_labels  = [measure.MeasureDate.strftime("%H:%M")]
            unit = measure.UnitOfMeasure
        else:
            data[name].append(measure.Value)
            x_labels.append(measure.MeasureDate.strftime("%H:%M"))    
    return draw_graph(data,  x_labels,  unit)

def daychart_temp(request,  year, month,  day):
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
    return draw_graph(data,  x_labels, "Degrees Celsius")


# Common function for line graphs
def draw_graph(data,  x_labels,  y_title):
    height = 300
    width = 800
    background = cairo.LinearGradient(300, 0, 300, 400)
    background.add_color_stop_rgb(0,0,0.4,0)
    #background.add_color_stop_rgb(1.0,0,0.1,0)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width,  height)
    #context = cairo.Context(surface)
    pp = cairoplot.DotLinePlot(surface = surface,
                               data = data, 
                               width = width, 
                               height = height, 
                               background = background, 
                               border = 0,  
                               x_labels = x_labels, 
                               axis = True, 
                               grid = True, 
                               dots = True,  
                               y_title = y_title, 
                               x_title = "Time", 
                               series_legend=True)
      # dash, y_labels, x_bounds, y_bounds,  series_colors 
    pp.render()
    response = HttpResponse(mimetype="image/png")
    pp.surface.write_to_png(response)
    return response

# Common function for bar graphs
def draw_bar_graph(data,  x_labels, y_labels):
    height = 300
    width = 800
    background = cairo.LinearGradient(300, 0, 300, 400)
    background.add_color_stop_rgb(0,0,0.4,0)
    #background.add_color_stop_rgb(1.0,0,0.1,0)
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width,  height)
    #context = cairo.Context(surface)
    pp = cairoplot.VerticalBarPlot(surface, 
                                   data, 
                                   width, 
                                   height, 
                                   background = background, 
                                   border = 20, 
                                   display_values = True, 
                                   grid = True,                
                                   rounded_corners = False,
                                   stack = False,
                                   three_dimension = False,
                                   series_labels = ['Energia cieplna [GJ]',
                                                    'Energia elektryczna [kWh]'],
                                   x_labels = x_labels, 
                                   y_labels = y_labels,
                                   x_bounds = None,
                                   y_bounds = None,
                                   series_colors  = [ (1,0.2,0), (1,0.7,0)]
                                   )                                        
    pp.render()
    response = HttpResponse(mimetype="image/png")
    pp.surface.write_to_png(response)
    return response

#=====================================================================
# Examples
#=====================================================================
def example1_chart(request,  name):
    height = 600
    width = 400
    data = { "john" : [-5, -2, 0, 1, 3], "mary" : [0, 0, 3, 5, 2], 
             "philip" : [-2, -3, -4, 2, 1] }
    x_labels = [ "jan/2008", "feb/2008", "mar/2008", 
                 "apr/2008", "may/2008" ]
    y_labels = [ "very low", "low", "medium", "high", "very high" ]
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, height, width)
    context = cairo.Context(surface)
    pp=cairoplot.DotLinePlot( surface, data, height, width, 
                              x_labels = x_labels, 
                              y_labels = y_labels, axis = True, grid = True,
                              x_title = "x axis", y_title = "y axis", 
                              series_legend=True )
    pp.render()
    response = HttpResponse(mimetype="image/png")
    pp.surface.write_to_png(response)
    return response
    
def example2_chart(request, name):
    data = {}
    x_labels = []
    for measure in Measure.objects.filter(Name = name).order_by('MeasureDate'):
        if data.get(name) == None:
            data[name] = [measure.Value]
            x_labels = [measure.MeasureDate.strftime("%Y/%m")]
        else:
            data[name].append(measure.Value)
            x_labels.append(measure.MeasureDate.strftime("%Y/%m"))    
    return draw_graph(data, x_labels)
