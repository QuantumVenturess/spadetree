from django.contrib import admin

from cities.models import City

class CityAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'state', 'created',)
    list_display_links = ('name',)
    list_filter = ('state',)
    search_fields = ('name',)

admin.site.register(City, CityAdmin)