from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = f'Welcome to Pharmacy Inventory System, {instance.first_name}!'
        message = f'''
        Hello {instance.first_name},
        
        Your account has been created with role: {instance.role}.
        
        Please keep your credentials secure.
        
        Best regards,
        Pharmacy Team
        '''
        send_mail(
            subject,
            message,
            'noreply@pharmacy.com',
            [instance.email],
            fail_silently=True,
        )