from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import User

class Prescription(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('FULFILLED', 'Fulfilled'),
        ('CANCELLED', 'Cancelled'),
        ('PARTIALLY_FULFILLED', 'Partially Fulfilled'),
    ]
    
    patient = models.ForeignKey(
        'medicines.Patient',
        on_delete=models.PROTECT,
        related_name='prescriptions'
    )
    prescribed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'role': 'DOCTOR'},
        related_name='issued_prescriptions'
    )
    fulfilled_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'PHARMACIST'},
        related_name='fulfilled_prescriptions'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    diagnosis = models.TextField(blank=True, help_text="Medical diagnosis or condition")
    notes = models.TextField(blank=True, help_text="Additional instructions or comments")
    is_urgent = models.BooleanField(default=False, help_text="Mark as urgent prescription")
    date_issued = models.DateTimeField(auto_now_add=True)
    date_fulfilled = models.DateTimeField(null=True, blank=True)
    date_cancelled = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-date_issued']
        indexes = [
            models.Index(fields=['patient', 'status']),
            models.Index(fields=['prescribed_by', 'date_issued']),
            models.Index(fields=['status', 'date_issued']),
        ]

    def clean(self):
        if self.status == 'FULFILLED' and not self.fulfilled_by:
            raise ValidationError("Fulfilled prescriptions must have a pharmacist assigned")
        if self.status == 'CANCELLED' and not self.date_cancelled:
            self.date_cancelled = timezone.now()

    def __str__(self):
        return f"Prescription #{self.id} - {self.patient}"

    def total_medicines(self):
        return self.prescription_medicines.count()

    def can_be_fulfilled(self):
        """Check if all medicines in prescription are available in stock"""
        for pm in self.prescription_medicines.all():
            if pm.medicine.quantity < pm.quantity:
                return False
        return True

class PrescriptionMedicine(models.Model):
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.CASCADE,
        related_name='prescription_medicines'
    )
    medicine = models.ForeignKey(
        'medicines.Medicine',
        on_delete=models.PROTECT,
        related_name='prescription_medicines'
    )
    quantity = models.PositiveIntegerField(default=1, help_text="Units prescribed")
    dosage_instructions = models.TextField(blank=True, help_text="Specific dosage instructions")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g., 7 days, 2 weeks")
    is_fulfilled = models.BooleanField(default=False)

    class Meta:
        unique_together = ['prescription', 'medicine']
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=1),
                name='min_prescribed_quantity'
            )
        ]

    def clean(self):
        if self.quantity > self.medicine.quantity:
            raise ValidationError(
                f"Only {self.medicine.quantity} units of {self.medicine.name} available in stock"
            )

    def __str__(self):
        return f"{self.medicine.name} x{self.quantity} for {self.prescription}"





