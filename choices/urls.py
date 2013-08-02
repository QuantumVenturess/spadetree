from django.conf.urls import patterns, url

urlpatterns = patterns('choices.views',
    url(r'^count.json/$', 'count'),
    url(r'^requests/$', 'requests'),
    url(r'^requests(?P<format>.json)/$', 'requests'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    url(r'^(?P<pk>\d+)/action/$', 'action'),
    url(r'^(?P<pk>\d+)/action(?P<format>.json)/$', 'action'),
    url(r'^(?P<pk>\d+)/new/note/$', 'new_note'),
)