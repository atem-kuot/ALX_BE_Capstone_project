from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import AlertLog
from medicines.models import Medicine
from prescriptions.models import Prescription

@receiver(post_save, sender=Medicine)
def create_stock_alerts(sender, instance, **kwargs):
    """Create alerts for low stock and expiry"""
    from django.db import transaction
    
    with transaction.atomic():
        # Low stock alert
        if instance.quantity <= instance.threshold_alert:
            alert_type = 'STOCK_CRITICAL' if instance.quantity == 0 else 'LOW_STOCK'
            AlertLog.objects.get_or_create(
                medicine=instance,
                alert_type=alert_type,
                is_resolved=False,
                defaults={
                    'title': f'{alert_type.replace("_", " ").title()}: {instance.name}',
                    'message': f'{instance.name} has {instance.quantity} units remaining '
                              f'(threshold: {instance.threshold_alert})',
                    'severity': 'CRITICAL' if instance.quantity == 0 else 'HIGH'
                }
            )
        
        # Expiry alert (30 days warning)
        if instance.expiry_date:
            days_until_expiry = (instance.expiry_date - timezone.now().date()).days
            if 0 <= days_until_expiry <= 30:
                alert_type = 'EXPIRED' if days_until_expiry < 0 else 'EXPIRY_WARNING'
                AlertLog.objects.get_or_create(
                    medicine=instance,
                    alert_type=alert_type,
                    is_resolved=False,
                    defaults={
                        'title': f'{alert_type.replace("_", " ").title()}: {instance.name}',
                        'message': f'{instance.name} expires on {instance.expiry_date} '
                                  f'({abs(days_until_expiry)} days)',
                        'severity': 'CRITICAL' if days_until_expiry < 0 else 'MEDIUM'
                    }
                )

@receiver(post_save, sender=Prescription)
def create_prescription_alerts(sender, instance, created, **kwargs):
    """Create alerts for prescriptions"""
    if created and instance.is_urgent:
        AlertLog.objects.create(
            prescription=instance,
            alert_type='PRESCRIPTION_URGENT',
            title=f'Urgent Prescription: {instance.patient}',
            message=f'Urgent prescription created for {instance.patient} by '
                   f'{instance.prescribed_by.get_full_name()}',
            severity='HIGH',
            user=instance.prescribed_by
        )
    
    # Alert for prescriptions pending for more than 24 hours
    if instance.status == 'PENDING' and not instance.is_urgent:
        hours_pending = (timezone.now() - instance.date_issued).total_seconds() / 3600
        if hours_pending > 24:
            AlertLog.objects.get_or_create(
                prescription=instance,
                alert_type='PRESCRIPTION_PENDING',
                is_resolved=False,
                defaults={
                    'title': f'Pending Prescription: {instance.patient}',
                    'message': f'Prescription for {instance.patient} has been '
                              f'pending for {int(hours_pending)} hours',
                    'severity': 'MEDIUM',
                    'user': {instance.prescribed_by},
                }
            )