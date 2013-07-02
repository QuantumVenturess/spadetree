from django.contrib import admin

from choices.models import Choice

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tutor', 'tutee', 'interest', 'created', 'accepted', 
        'denied', 'completed', 'date_completed', 'content', 'tutor_viewed',
            'tutee_viewed', 'day', 'hour', 'date', 'address', 'city', 'state',)
    list_display_links = ('tutee', 'tutor',)
    search_fields = ('tutee', 'tutor',)

admin.site.register(Choice, ChoiceAdmin)