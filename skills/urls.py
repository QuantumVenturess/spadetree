from django.conf.urls import patterns, url

urlpatterns = patterns('skills.views',
    url(r'^(?P<pk>\d+)/delete/$', 'delete'),
    url(r'^(?P<pk>\d+)/delete(?P<format>.(js|json))/$', 'delete'),
    url(r'^new/$', 'new'),
    url(r'^new(?P<format>.(js|json))/$', 'new'),
)