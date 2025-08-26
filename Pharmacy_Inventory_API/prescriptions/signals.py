from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from .models import Prescription

@receiver(post_save, sender=Prescription)
def notify_urgent_prescription(sender, instance, created, **kwargs):
    """Notify admins about urgent prescriptions"""
    if created and instance.is_urgent:
        subject = f'URGENT: New prescription for {instance.patient}'
        message = f'''
        Urgent prescription created by Dr. {instance.prescribed_by.get_full_name()}
        
        Patient: {instance.patient}
        Diagnosis: {instance.diagnosis}
        
        Please prioritize this prescription.
        '''
        mail_admins(subject, message, fail_silently=True)