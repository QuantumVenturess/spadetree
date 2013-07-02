from django.conf.urls import patterns, url

urlpatterns = patterns('days.views',
    url(r'^(?P<pk>[\d]+)/free/$', 'free'),
)