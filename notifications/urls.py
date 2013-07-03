from django.conf.urls import patterns, url

urlpatterns = patterns('notifications.views',
    url(r'^$', 'list'),
)