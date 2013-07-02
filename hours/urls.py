from django.conf.urls import patterns, url

urlpatterns = patterns('hours.views',
    url(r'^(?P<pk>[\d]+)/free/$', 'free'),
)