from django.contrib import admin

from skills.models import Skill

class SkillAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'interest', 'created',)
    list_display_links = ('user', 'interest',)
    list_filter = ('interest',)
    search_fields = ('interst', 'user',)

admin.site.register(Skill, SkillAdmin)