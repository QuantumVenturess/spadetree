from django.contrib import admin
from django.contrib.auth.models import User
from users.models import Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display  = ('user', 'about', 'city', 'tutee', 'tutor', 'in_count', 
      'phone', 'slug',)
    search_fields = ('user',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'is_staff', 'date_joined', 
        'last_login',)
    list_display_links = ('username',)
    search_fields = ('email', 'first_name', 'last_name', 'username',)

admin.site.register(Profile, ProfileAdmin)
admin.site.unregister(User)
admin.site.register(User, UserAdmin)