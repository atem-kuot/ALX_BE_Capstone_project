from django.contrib import admin
from .models import AlertLog, AlertPreference

@admin.register(AlertLog)
class AlertLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'alert_type', 'severity', 'title', 'is_resolved', 'created_at']
    list_filter = ['alert_type', 'severity', 'is_resolved', 'created_at']
    search_fields = ['title', 'message', 'medicine__name']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_resolved']
    
    fieldsets = (
        ('Alert Details', {
            'fields': ('alert_type', 'severity', 'title', 'message')
        }),
        ('Related Objects', {
            'fields': ('medicine', 'prescription', 'user'),
            'classes': ('collapse',)
        }),
        ('Resolution', {
            'fields': ('is_resolved', 'resolved_by', 'resolved_at', 'resolved_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AlertPreference)
class AlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'min_severity_level']
    list_filter = ['email_notifications', 'push_notifications', 'daily_digest']
    search_fields = ['user__username', 'user__email']