from django.contrib import admin
from .models import Profile, Event, Event,Notification,Attendance,Invitation
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')  # Customize the fields displayed in the admin list view
    list_filter = ('user__username',)  # Add filters for user's username
    search_fields = ('user__username', 'bio')  # Add search fields for user's username and bio

admin.site.register(Event)
admin.site.register(Notification)
admin.site.register(Attendance)
admin.site.register(Invitation)
