from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('polls.views',
    # url(r'^$', 'polls.views.home', name='home'),
    (r'^$', 'index'),
    (r'^yeartemp/(?P<year>\w+)/$', 'yeartemp'),
    (r'^yearenergy/(?P<year>\w+)/$', 'yearenergy'),
    (r'^photos/$', 'photos'),
    (r'^daytemp/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 
     'daytemp'),
    (r'^monthtemp/(?P<year>\w+)/(?P<month>\w+)/$', 'monthtemp'),
    (r'^monthenergy/(?P<year>\w+)/(?P<month>\w+)/$', 'monthenergy'),
    (r'^dayenergy/(?P<year>\w+)/(?P<month>\w+)/(?P<day>\w+)/$', 'dayenergy'),
    (r'^selectmonth/$', 'selectmonth'),
    (r'^selectmonth_energy/$', 'selectmonth_energy'),
    (r'^selectday/$', 'selectday'),
    (r'^selectday_energy/$', 'selectday_energy'),
    (r'^contact/$', 'contact'),
    (r'^costs/$', 'costs'),
    (r'^insert/$', 'handle_value'),
    (r'^update_temp/(?P<id>\w+)/$', 'update_temp')
)

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
)
