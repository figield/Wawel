from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('polls.views',
    # url(r'^$', 'polls.views.home', name='home'),
    (r'^$', 'index'),
    (r'^wykresy/$', 'yearreport'),
    (r'^zdjecia/$', 'photos'),
    (r'^allmeasures/$', 'all_measures'),
    (r'^update_temp/(?P<id>\w+)/$', 'update_temp'),
    (r'^dayreport/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 
     'dayreport'),
    (r'^monthreport/(?P<year>\w+)/(?P<month>\w+)/$', 'monthreport'),
    (r'^pomiar/(?P<measure_id>\d+)/$', 'detail'),
    (r'^insert/$', 'handle_value'),
)

urlpatterns += patterns('polls.viewsgraphs',
    (r'^generateChart/(?P<name>\w+)/$', 
     'yearchart'),
    (r'^generateTempChart/$', 
     'yearchart_temp'),
    (r'^daychart/(?P<name>\w+)/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$',
     'daychart'),
    (r'^dayTempChart/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 
     'daychart_temp'),
    (r'^monthchart/(?P<name>\w+)/(?P<year>\w+)/(?P<month>\w+)/$', 
     'monthchart'),
    (r'^monthTempChart/(?P<year>\w+)/(?P<month>\w+)/$', 
     'monthchart_temp'),
    (r'^monthElecBarChart/(?P<year>\w+)/(?P<month>\w+)/$', 
     'month_barchart')
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
