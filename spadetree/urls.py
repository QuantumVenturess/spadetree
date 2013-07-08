from django.conf import settings
from django.conf.urls import include, patterns, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # Root path = Join page
    url(r'^$', 'sessions.views.join', name='root_path'),

    # Pages (static)
    url(r'^about/$', 'pages.views.about'),

    # Admin
    url(r'^admin/', include(admin.site.urls)),
    # Choices
    url(r'^c/', include('choices.urls')),
    # Cities
    url(r'^cities/', include('cities.urls')),
    # Days
    url(r'^d/', include('days.urls')),
    # Hours
    url(r'^h/', include('hours.urls')),
    # Interests
    url(r'^i/', include('interests.urls')),
    # Notifications
    url(r'^n/', include('notifications.urls')),
    # OAuth
    url(r'^oauth/', include('oauth.urls')),
    # Sessions
    url(r'^join/$', 'sessions.views.join'),
    url(r'^sessions/', include('sessions.urls')),
    # Skills
    url(r'^skills/', include('skills.urls')),
    # States
    url(r'^states/', include('states.urls')),
    # User Messages
    url(r'^m/', include('usermessages.urls')),
    # Users
    url(r'^u/', include('users.urls')),
)

if not settings.DEV:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', { 
            'document_root': settings.STATIC_ROOT })
    )