from django.contrib import admin
from reviews.models import Review

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'created', 'tutee', 'tutor', 'content', 'positive',)
    list_display_links = ('created',)
    list_filter = ('tutee', 'tutor',)
    search_fields = ('content',)

admin.site.register(Review, ReviewAdmin)