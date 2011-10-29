from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('polls.views',
    # url(r'^$', 'polls.views.home', name='home'),
    (r'^$', 'index'),
    (r'^include/$', 'include'),
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
    (r'^heating/$', 'heating'),
    (r'^costs/$', 'costs'),
    (r'^insert/$', 'handle_value'),
    (r'^update_temp/(?P<id>\w+)/$', 'update_temp'),
    (r'^update_temp2/(?P<id>\w+)/$', 'update_temp2'),
    (r'^admin/', include(admin.site.urls)),
    (r'^(?P<fake>\w+)/$', 'anyrequest')
)

