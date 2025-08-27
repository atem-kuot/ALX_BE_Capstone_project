from django.core.management.base import BaseCommand
from django.utils import timezone
from alerts.models import AlertLog
from core.telegram_service import TelegramBotService

class Command(BaseCommand):
    help = 'Send daily digest of unresolved alerts via Telegram'
    
    def handle(self, *args, **options):
        # Get unresolved alerts from the last 24 hours
        twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)
        
        unresolved_alerts = AlertLog.objects.filter(
            is_resolved=False,
            created_at__gte=twenty_four_hours_ago
        )
        
        telegram_service = TelegramBotService()
        
        if telegram_service.is_configured():
            success = telegram_service.send_daily_digest(unresolved_alerts)
            if success:
                self.stdout.write(
                    self.style.SUCCESS('Daily digest sent successfully via Telegram')
                )
            else:
                self.stdout.write(
                    self.style.ERROR('Failed to send daily digest via Telegram')
                )
        else:
            self.stdout.write(
                self.style.WARNING('Telegram bot not configured. Skipping daily digest.')
            )