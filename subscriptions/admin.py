from django.contrib import admin

from subscriptions.models import Subscription

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'channel', 'user',)
    list_display_links = ('pk', 'created',)

admin.site.register(Subscription, SubscriptionAdmin)