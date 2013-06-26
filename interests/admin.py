from django.contrib import admin

from interests.models import Interest

class InterestAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'created',)
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(Interest, InterestAdmin)