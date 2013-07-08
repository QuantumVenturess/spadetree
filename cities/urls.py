from django.conf.urls import patterns, url

urlpatterns = patterns('cities.views',
    url(r'^city-list/$', 'city_list'),
    url(r'^city-list/(?P<name>[-\w]+)/$', 'city_list'),
)