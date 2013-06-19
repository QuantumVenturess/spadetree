from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Root path
    url(r'^$', 'users.views.join', name='root_path'),
    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # OAuth
    url(r'^oauth/', include('oauth.urls')),
    # Sessions
    url(r'^sessions/', include('sessions.urls')),
    # Users
    url(r'^join/$', 'users.views.join'),
    url(r'^u/', include('users.urls')),
)
