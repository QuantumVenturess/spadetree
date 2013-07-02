from django.contrib import admin

from hours.models import Hour, HourFree

class HourAdmin(admin.ModelAdmin):
    list_display = ('pk', 'value',)

class HourFreeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'hour',)
    list_display_links = ('user',)
    list_filter = ('hour',)

admin.site.register(Hour, HourAdmin)
admin.site.register(HourFree, HourFreeAdmin)