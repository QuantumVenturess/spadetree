from django.conf.urls import patterns, url

urlpatterns = patterns('states.views',
    url(r'^state-list/$', 'state_list'),
)