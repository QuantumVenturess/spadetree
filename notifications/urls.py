from django.conf.urls import patterns, url

urlpatterns = patterns('notifications.views',
    url(r'^count.json/$', 'count'),
    url(r'^$', 'list'),
    url(r'^notifications/$', 'notifications'),
    url(r'^notifications(?P<format>.json)/$', 'notifications'),
)