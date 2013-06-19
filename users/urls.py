from django.conf.urls import patterns, url

urlpatterns = patterns('users.views',
    url(r'^choose/$', 'choose'),
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
)