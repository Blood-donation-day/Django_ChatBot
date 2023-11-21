from django.contrib import admin
from .models import User, Profile
from chatting.models import Ticket
# from django.utils.safestring import mark_safe


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 0  # 티켓을 몇 개까지 추가할지 설정
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'get_profile_username', 'get_ticket_remain']
    list_filter = ['created_at', 'updated_at']
    list_display_links = ['email']
    fields = ['email','is_staff', 'is_active']
    list_per_page = 20
    
    inlines = [TicketInline]
    def get_profile_username(self, obj):
        return obj.profile.username if obj.profile else None
    
    get_profile_username.short_description = 'username'
    
    def get_ticket_remain(self, obj):
        ticket = obj.ticket.first()
        return ticket.today_limit if ticket else None
    
    get_ticket_remain.short_description = 'tickets'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['get_user_email', 'username', 'introduce']
    list_filter = ['id']
    list_per_page = 20
    
    
    def get_user_email(self, obj):
        return obj.user.email
    
    get_user_email.short_description = 'email'
    