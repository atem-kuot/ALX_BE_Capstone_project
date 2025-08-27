from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class AlertLog(models.Model):
    ALERT_TYPES = [
        ('LOW_STOCK', 'Low Stock'),
        ('EXPIRY_WARNING', 'Expiry Warning'),
        ('EXPIRED', 'Expired'),
        ('PRESCRIPTION_URGENT', 'Urgent Prescription'),
        ('PRESCRIPTION_PENDING', 'Pending Prescription'),
        ('STOCK_CRITICAL', 'Critical Stock'),
        ('SYSTEM', 'System Alert'),
    ]
    
    SEVERITY_LEVELS = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPES)
    severity = models.CharField(max_length=20, choices=SEVERITY_LEVELS, default='MEDIUM')
    title = models.CharField(max_length=200)
    message = models.TextField()
    
    # Optional foreign keys for related objects
    medicine = models.ForeignKey(
        'medicines.Medicine',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alerts'
    )
    prescription = models.ForeignKey(
        'prescriptions.Prescription',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='alerts'
    )
    user = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='alerts'
    )
    
    is_resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(
        'core.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='resolved_alerts'
    )
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['alert_type', 'is_resolved']),
            models.Index(fields=['severity', 'created_at']),
            models.Index(fields=['medicine', 'is_resolved']),
            models.Index(fields=['is_resolved', 'created_at']),
        ]

    def __str__(self):
        return f"{self.get_alert_type_display()} - {self.title}"

    def clean(self):
        # Set severity based on alert type
        if not self.severity:
            if self.alert_type in ['STOCK_CRITICAL', 'EXPIRED']:
                self.severity = 'CRITICAL'
            elif self.alert_type in ['LOW_STOCK', 'PRESCRIPTION_URGENT']:
                self.severity = 'HIGH'
            elif self.alert_type in ['EXPIRY_WARNING']:
                self.severity = 'MEDIUM'
            else:
                self.severity = 'LOW'

    def resolve(self, user, notes=""):
        self.is_resolved = True
        self.resolved_by = user
        self.resolved_at = timezone.now()
        self.resolved_notes = notes
        self.save()

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        # Send Telegram notification for new unresolved alerts
        if is_new and not self.is_resolved:
            self.send_telegram_notification()
    
    def send_telegram_notification(self):
        """Send notification via Telegram"""
        from core.telegram_service import TelegramBotService
        telegram_service = TelegramBotService()
        
        # Check user preferences if this is a user-specific alert
        if self.user:
            try:
                preferences = self.user.alert_preferences
                if not (preferences.push_notifications and preferences.immediate_alerts):
                    return False
            except AlertPreference.DoesNotExist:
                pass  # Send by default if no preferences set
        
        return telegram_service.send_alert_notification(self)



class AlertPreference(models.Model):
    user = models.OneToOneField(
        'core.User',
        on_delete=models.CASCADE,
        related_name='alert_preferences'
    )
    
    # Notification methods
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    
    # Alert type preferences
    receive_low_stock_alerts = models.BooleanField(default=True)
    receive_expiry_alerts = models.BooleanField(default=True)
    receive_prescription_alerts = models.BooleanField(default=True)
    receive_system_alerts = models.BooleanField(default=True)
    
    # Severity filters
    min_severity_level = models.CharField(
        max_length=20,
        choices=AlertLog.SEVERITY_LEVELS,
        default='MEDIUM'
    )
    
    # Frequency settings
    daily_digest = models.BooleanField(default=True)
    immediate_alerts = models.BooleanField(default=True)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Alert Preference"
        verbose_name_plural = "Alert Preferences"

    def __str__(self):
        return f"Alert preferences for {self.user.username}"

    telegram_notifications = models.BooleanField(
        default=True,
        help_text="Receive alerts via Telegram bot"
    )
    telegram_chat_id = models.CharField(
        max_length=50,
        blank=True,
        help_text="Personal Telegram chat ID for direct notifications"
    )
