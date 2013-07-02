from django.contrib import admin

from days.models import Day, DayFree

class DayAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'value',)
    list_display_links = ('pk', 'name',)

class DayFreeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'day',)
    list_display_links = ('user',)
    list_filter = ('day',)

admin.site.register(Day, DayAdmin)
admin.site.register(DayFree, DayFreeAdmin)