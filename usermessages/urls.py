from django.conf.urls import patterns, url

urlpatterns = patterns('usermessages.views',
    url(r'^count.json/$', 'count'),
    url(r'^(?P<pk>[\d]+)/$', 'detail'),
    url(r'^(?P<pk>[\d]+)(?P<format>.json)/$', 'detail'),
    url(r'^messages/$', 'list'),
    url(r'^messages(?P<format>.json)/$', 'list'),
    url(r'^(?P<pk>[\d]+)/new/$', 'new'),
    url(r'^(?P<pk>[\d]+)/new(?P<format>.json)/$', 'new'),
)