from django.conf.urls import patterns, url

urlpatterns = patterns('oauth.views',
    url(r'^authenticate-app(?P<format>.json)/$', 'authenticate_app'),
    url(r'^facebook/$', 'facebook'),
    url(r'^facebook/authenticate/$', 'facebook_authenticate'),
)