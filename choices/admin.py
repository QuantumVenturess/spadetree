from django.contrib import admin

from choices.models import Choice, ChoiceNote

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tutor', 'tutee', 'interest', 'created', 'accepted', 
        'denied', 'completed', 'date_completed', 'content', 'tutor_viewed',
            'tutee_viewed', 'day', 'hour', 'date', 'address', 'city', 'state',)
    list_display_links = ('tutee', 'tutor',)
    search_fields = ('tutee', 'tutor',)

class ChoiceNoteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'choice', 'content',)
    list_display_links = ('pk', 'user',)
    search_fields = ('content',)

admin.site.register(Choice, ChoiceAdmin)
admin.site.register(ChoiceNote, ChoiceNoteAdmin)