import requests
import logging
from django.conf import settings
from django.utils import timezone
from alerts.models import AlertLog

logger = logging.getLogger(__name__)

class TelegramBotService:
    def __init__(self):
        self.bot_token = getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
        self.chat_id = getattr(settings, 'TELEGRAM_CHAT_ID', None)
        self.base_url = f"https://api.telegram.org/bot{self.bot_token}"
    
    def is_configured(self):
        return bool(self.bot_token and self.chat_id)
    
    def send_message(self, message, parse_mode='HTML', disable_web_page_preview=True):
        """Send message to Telegram channel"""
        if not self.is_configured():
            logger.warning("Telegram bot not configured. Skipping message.")
            return False
        
        try:
            url = f"{self.base_url}/sendMessage"
            payload = {
                'chat_id': self.chat_id,
                'text': message,
                'parse_mode': parse_mode,
                'disable_web_page_preview': disable_web_page_preview
            }
            
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            
            logger.info(f"Telegram message sent successfully: {message[:100]}...")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending Telegram message: {e}")
            return False
    
    def send_alert_notification(self, alert):
        """Send formatted alert notification"""
        if not self.is_configured():
            return False
        
        emoji = self._get_alert_emoji(alert.severity)
        timestamp = timezone.localtime(alert.created_at).strftime('%Y-%m-%d %H:%M')
        
        message = f"""
{emoji} <b>{alert.get_severity_display().upper()} ALERT</b> {emoji}

<b>Type:</b> {alert.get_alert_type_display()}
<b>Title:</b> {alert.title}
<b>Time:</b> {timestamp}

<b>Message:</b>
{alert.message}
        """
        
        if alert.medicine:
            message += f"\n<b>Medicine:</b> {alert.medicine.name}"
        if alert.prescription:
            message += f"\n<b>Prescription:</b> #{alert.prescription.id}"
        
        message += f"\n\n<code>Alert ID: {alert.id}</code>"
        
        return self.send_message(message.strip())
    
    def send_daily_digest(self, alerts):
        """Send daily digest of unresolved alerts"""
        if not self.is_configured() or not alerts:
            return False
        
        critical_count = sum(1 for a in alerts if a.severity == 'CRITICAL')
        high_count = sum(1 for a in alerts if a.severity == 'HIGH')
        total_count = len(alerts)
        
        message = f"""
📊 <b>DAILY ALERT DIGEST</b>
⏰ {timezone.localtime().strftime('%Y-%m-%d')}

🚨 <b>Critical:</b> {critical_count}
⚠️ <b>High:</b> {high_count}
📋 <b>Total Unresolved:</b> {total_count}

<b>Breakdown by Type:</b>
        """
        
        # Count by alert type
        from collections import Counter
        type_counts = Counter(alert.alert_type for alert in alerts)
        
        for alert_type, count in type_counts.items():
            alert_display = dict(AlertLog.ALERT_TYPES).get(alert_type, alert_type)
            message += f"\n• {alert_display}: {count}"
        
        message += f"\n\n📋 <i>View all alerts in the system</i>"
        
        return self.send_message(message.strip())
    
    def _get_alert_emoji(self, severity):
        """Get appropriate emoji for severity level"""
        emoji_map = {
            'CRITICAL': '🚨',
            'HIGH': '⚠️',
            'MEDIUM': '🔸',
            'LOW': '🔹'
        }
        return emoji_map.get(severity, '📌')