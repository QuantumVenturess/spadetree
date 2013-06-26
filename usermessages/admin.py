from django.contrib import admin

from usermessages.models import UserMessage

class UserMessageAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'sender', 'recipient', 'content', 'viewed')
    list_display_links = ('created',)
    search_fields = ('content',)

admin.site.register(UserMessage, UserMessageAdmin)