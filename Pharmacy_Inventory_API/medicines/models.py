from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from core.models import User


# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100, help_text="Supplier company name")
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True, help_text="Primary contact email")
    phone = models.CharField(max_length=20, help_text="Format: +1234567890")
    address = models.TextField(help_text="Full physical address")
    
    Date_Added = models.DateTimeField(auto_now_add=True)
    Last_Updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

# Medicine Model
class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('ANTIBIOTIC', 'Antibiotic'),
        ('ANALGESIC', 'Analgesic (Pain Reliever)'),
        ('ANTIVIRAL', 'Antiviral'),
        ('ANTIFUNGAL', 'Antifungal'),
        ('ANTIPARASITIC', 'Antiparasitic'),
        ('ANTIDEPRESSANT', 'Antidepressant'),
        ('ANTIPSYCHOTIC', 'Antipsychotic'),
        ('ANTIHISTAMINE', 'Antihistamine'),
        ('BRONCHODILATOR', 'Bronchodilator'),
        ('CORTICOSTEROID', 'Corticosteroid'),
        ('DIURETIC', 'Diuretic'),
        ('ANTIHYPERTENSIVE', 'Antihypertensive'),
        ('ANTIDIABETIC', 'Antidiabetic'),
        ('ANTICOAGULANT', 'Anticoagulant'),
        ('ANTIPLATELET', 'Antiplatelet'),
        ('LIPID_LOWERING', 'Lipid-Lowering'),
        ('HORMONE', 'Hormone'),
        ('IMMUNOSUPPRESSANT', 'Immunosuppressant'),
        ('VACCINE', 'Vaccine'),
        ('VITAMIN_SUPPLEMENT', 'Vitamin & Supplement'),
        ('MINERAL', 'Mineral'),
        ('ELECTROLYTE', 'Electrolyte'),
        ('GASTROINTESTINAL', 'Gastrointestinal'),
        ('OPHTHALMIC', 'Ophthalmic'),
        ('OTIC', 'Otic (Ear)'),
        ('TOPICAL', 'Topical'),
        ('DERMATOLOGICAL', 'Dermatological'),
        ('CONTRACEPTIVE', 'Contraceptive'),
        ('UROLOGICAL', 'Urological'),
        ('ONCOLOGY', 'Oncology'),
        ('ANESTHETIC', 'Anesthetic'),
        ('SEDATIVE', 'Sedative'),
        ('STIMULANT', 'Stimulant'),
        ('ANTACID', 'Antacid'),
        ('LAXATIVE', 'Laxative'),
        ('ANTIDIARRHEAL', 'Antidiarrheal'),
        ('ANTIEMETIC', 'Antiemetic'),
        ('ANTIULCER', 'Antiulcer'),
        ('CARDIAC', 'Cardiac'),
        ('RESPIRATORY', 'Respiratory'),
        ('NEUROLOGICAL', 'Neurological'),
        ('PSYCHIATRIC', 'Psychiatric'),
        ('RHEUMATOLOGICAL', 'Rheumatological'),
        ('OTHER', 'Other'),
    ]
    name = models.CharField(max_length=100, help_text="Brand or generic name")
    description = models.TextField(blank=True, help_text="Additional details about the medicine")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    quantity = models.PositiveIntegerField(default=0, help_text="Current stock count")
    dosage = models.CharField(max_length=50, help_text="e.g., 500mg/tablet, 10mg/ml")
    expiry_date = models.DateField(help_text="Format: YYYY-MM-DD")
    threshold_alert = models.PositiveIntegerField(
        default=10, 
        help_text="Low stock warning level"
    )
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.PROTECT,
        related_name='medicines',
        help_text="Primary supplier for this medicine"
    )
    is_active = models.BooleanField(default=True)
    
    Date_Added = models.DateTimeField(auto_now_add=True)
    Last_Updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name='non_negative_quantity'
            ),
            models.CheckConstraint(
                check=models.Q(expiry_date__gt=timezone.now().date()),
                name='valid_expiry_date'
            )
        ]

    def clean(self):
        if self.expiry_date <= timezone.now().date():
            raise ValidationError("Expiry date must be in the future")
        if self.quantity < 0:
            raise ValidationError("Quantity cannot be negative")

    def __str__(self):
        return f"{self.name} ({self.dosage})"

    def get_category_display_name(self):
        """Helper method to get the full display name of the category"""
        return dict(self.CATEGORY_CHOICES).get(self.category, self.category)
 
    def update_quantity(self, change_amount, action, user, reason="", prescription=None):
        """Safe method to update quantity with logging"""
        from django.db import transaction
        
        with transaction.atomic():
            previous_quantity = self.quantity
            self.quantity += change_amount
            
            if self.quantity < 0:
                raise ValidationError("Insufficient stock")
            
            self.save()
            
            # Create inventory log
            InventoryLog.objects.create(
                medicine=self,
                action=action,
                quantity_change=change_amount,
                previous_quantity=previous_quantity,
                new_quantity=self.quantity,
                performed_by=user,
                reason=reason,
                prescription=prescription
            )
        
        return self.quantity


class InventoryLog(models.Model):
    ACTION_CHOICES = [
        ('STOCK_ADD', 'Stock Added'),
        ('STOCK_REMOVE', 'Stock Removed'),
        ('STOCK_ADJUST', 'Stock Adjusted'),
        ('PRESCRIPTION_FULFILL', 'Prescription Fulfilled'),
        ('PRESCRIPTION_CANCELLED', 'Prescription Cancelled'),
        ('DISCARDED', 'Discarded (Expired/Damaged)'),
        ('RECEIVED', 'Received from Supplier'),
    ]
    
    medicine = models.ForeignKey(
        'Medicine',
        on_delete=models.CASCADE,
        related_name='inventory_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    quantity_change = models.IntegerField(help_text="Positive for additions, negative for removals")
    previous_quantity = models.IntegerField(help_text="Quantity before change")
    new_quantity = models.IntegerField(help_text="Quantity after change")
    performed_by = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='inventory_changes'
    )
    reason = models.TextField(blank=True, help_text="Reason for the change")
    prescription = models.ForeignKey(
        'prescriptions.Prescription',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='inventory_logs'
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['medicine', 'timestamp']),
            models.Index(fields=['performed_by', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.get_action_display()} - {self.medicine.name} ({self.quantity_change})"

class Patient(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('U', 'Unknown'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='U')
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)
    emergency_phone = models.CharField(max_length=20, blank=True)
    medical_history = models.TextField(blank=True)
    allergies = models.TextField(blank=True)
    
    Date_Added = models.DateTimeField(auto_now_add=True)
    Last_Updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['first_name', 'last_name', 'date_of_birth']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"