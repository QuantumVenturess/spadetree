from django.contrib import admin
from oauth.models import Oauth

class OauthAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'provider', 'facebook_id',)
    list_display_links = ('user',)
    list_filter = ('provider',)
    search_fields = ('user',)

admin.site.register(Oauth, OauthAdmin)