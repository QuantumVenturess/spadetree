from django.contrib import admin
from states.models import State

class StateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'created',)
    list_display_links = ('name',)
    search_fields = ('name',)

admin.site.register(State, StateAdmin)