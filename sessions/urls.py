from django.conf.urls import patterns, url

urlpatterns = patterns('sessions.views',
    url(r'^sign-out/$', 'sign_out'),
)