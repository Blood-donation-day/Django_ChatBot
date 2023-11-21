from django.contrib import admin
from .models import User, Profile
# from django.utils.safestring import mark_safe

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'get_profile_username']
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['email']
    fields = ['email','is_staff', 'is_active']
    list_per_page = 20
    
    def get_profile_username(self, obj):
        return obj.profile.username if obj.profile else None
    
    get_profile_username.short_description = 'username'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user_email', 'username', 'introduce']
    list_filter = ['id']
    list_per_page = 20
    
    
    def get_user_email(self, obj):
        return obj.user.email
    
    get_user_email.short_description = 'email'
    
