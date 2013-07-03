from django.contrib import admin

from notifications.models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'channel', 'user', 'users_viewed', 
        'model', 'action', 'choice_note',)
    list_display_links = ('pk', 'created',)

admin.site.register(Notification, NotificationAdmin)