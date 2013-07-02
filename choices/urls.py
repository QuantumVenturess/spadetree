from django.conf.urls import patterns, url

urlpatterns = patterns('choices.views',
    url(r'^requests/$', 'requests'),
    url(r'^(?P<pk>\d+)/$', 'detail'),
    url(r'^(?P<pk>\d+)/action/$', 'action'),
    url(r'^(?P<pk>\d+)/new/note/$', 'new_note'),
)