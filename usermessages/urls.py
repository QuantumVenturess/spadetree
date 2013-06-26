from django.conf.urls import patterns, url

urlpatterns = patterns('usermessages.views',
    url(r'^(?P<pk>[\d]+)/$', 'detail'),
    url(r'^messages/$', 'list'),
    url(r'^(?P<pk>[\d]+)/new/$', 'new'),
)