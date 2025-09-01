from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('DOCTOR', 'Doctor'),
        ('PHARMACIST', 'Pharmacist'), 
        ('ADMIN', 'Admin')
    ]
    
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    
    def clean(self):
        if self.role == 'DOCTOR' and not self.phone:
            raise ValidationError("Doctors must have a phone number for emergency contact.")
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['email'],
                name='unique_user_email'
            )
        ]
    
    def __str__(self):
        return f"{self.username} ({self.role})"
# Create your models here.
