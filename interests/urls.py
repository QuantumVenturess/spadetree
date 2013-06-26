from django.conf.urls import patterns, url

urlpatterns = patterns('interests.views',
    url(r'^browse/$', 'browse'),
    url(r'^browse/search/$', 'browse_search'),
    url(r'^browse/search(?P<format>.(js|json))/$', 'browse_search'),
    url(r'^search(?P<format>.(js|json))/$', 'search'),
    # Detail
    url(r'^(?P<slug>[-\w]+)/$', 'detail'),
)