from django.contrib import admin
from .models import Profile, Like


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'age', 'location', 'is_active', 'date_created')
    list_filter = ('gender', 'religion', 'is_active', 'date_created')
    search_fields = ('user__username', 'user__email', 'location')
    readonly_fields = ('date_created', 'date_updated')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('from_user__username', 'to_user__username')
