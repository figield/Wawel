from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('polls.views',
    # url(r'^$', 'polls.views.home', name='home'),
    (r'^$', 'index'),
    (r'^yeartemp/(?P<year>\w+)/$', 'yeartemp2'),
    (r'^yearenergy/(?P<year>\w+)/$', 'yearenergy'),
    (r'^photos/$', 'photos'),
    (r'^update_temp/(?P<id>\w+)/$', 'update_temp'),
    (r'^dayreport/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 
     'dayreport'),
    (r'^daytemp/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 
     'daytemp'),
    (r'^selectday/$', 'selectday'),
    (r'^monthreport/(?P<year>\w+)/(?P<month>\w+)/$', 'monthreport'),
    (r'^monthtemp/(?P<year>\w+)/(?P<month>\w+)/$', 'monthtemp'),
    (r'^monthenergy/(?P<year>\w+)/(?P<month>\w+)/$', 'monthenergy'),
    (r'^selectmonth/$', 'selectmonth'),
    (r'^contact/$', 'contact'),
    (r'^costs/$', 'costs'),
    (r'^insert/$', 'handle_value'),
)

urlpatterns += patterns('polls.viewsgraphs',
    (r'^generateTempChart/$', 
     'yearchart_temp_in_out'),
    (r'^dayTempChart/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 
     'daychart_temp'),
    (r'^monthchart/(?P<name>\w+)/(?P<year>\w+)/(?P<month>\w+)/$', 
     'monthchart'),
    (r'^monthTempChart/(?P<year>\w+)/(?P<month>\w+)/$', 
     'monthchart_temp_in_out'),
    (r'^monthElecBarChart/(?P<year>\w+)/(?P<month>\w+)/$', 
     'month_barchart'),
    (r'^yearElecBarChart/(?P<year>\w+)/$', 
     'year_barchart')
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
