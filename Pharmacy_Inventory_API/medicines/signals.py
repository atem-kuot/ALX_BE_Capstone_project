from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from .models import Medicine
from django.utils import timezone
from alerts.models import AlertLog

@receiver(post_save, sender=Medicine)
def check_low_stock(sender, instance, **kwargs):
    if instance.quantity <= instance.threshold_alert:
        AlertLog.objects.create(
            medicine=instance,
            alert_type='LOW_STOCK',
            message=f'Low stock alert for {instance.name}. Current quantity: {instance.quantity}'
        )

@receiver(post_save, sender=Medicine)
def check_expiry(sender, instance, **kwargs):
    if instance.expiry_date <= timezone.now().date() + timezone.timedelta(days=30):
        AlertLog.objects.create(
            medicine=instance,
            alert_type='EXPIRY',
            message=f'Medicine {instance.name} expires on {instance.expiry_date}'
        )


@receiver(post_save, sender='prescriptions.PrescriptionMedicine')
def log_prescription_fulfillment(sender, instance, created, **kwargs):
    if created and instance.prescription.status == 'FULFILLED':
        medicine = instance.medicine
        medicine.update_quantity(
            change_amount=-instance.quantity,
            action='PRESCRIPTION_FULFILL',
            user=instance.prescription.fulfilled_by,  # Add this field to Prescription
            reason=f'Prescription #{instance.prescription.id} fulfillment',
            prescription=instance.prescription
        )