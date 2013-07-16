from django.contrib import admin

from channels.models import Channel

class ChannelAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'choice', 'interest', 'subscription_count',
      'notification_count',)
    list_display_links = ('pk', 'created',)

admin.site.register(Channel, ChannelAdmin)