from rest_framework import serializers
from .models import Medicine, Supplier
from rest_framework import serializers
from .models import Medicine, Supplier, InventoryLog, Patient
from prescriptions.models import Prescription

class SupplierSerializer(serializers.ModelSerializer):
    medicine_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = [
            'id', 'name', 'contact_person', 'email', 'phone', 'address',
            'Date_Added', 'Last_Updated', 'medicine_count'
        ]
        read_only_fields = ('Date_Added', 'Last_Updated', 'medicine_count')
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': 'Supplier name cannot be blank.',
                    'max_length': 'Name cannot be longer than 100 characters.'
                }
            },
            'contact_person': {
                'required': True,
                'error_messages': {
                    'blank': 'Contact person name is required.',
                    'max_length': 'Contact person name is too long.'
                }
            },
            'email': {
                'required': True,
                'error_messages': {
                    'blank': 'Email address is required.',
                    'invalid': 'Enter a valid email address.'
                }
            },
            'phone': {
                'required': True,
                'error_messages': {
                    'blank': 'Phone number is required.'
                }
            },
            'address': {
                'required': True,
                'error_messages': {
                    'blank': 'Address is required.'
                }
            }
        }
    
    def get_medicine_count(self, obj):
        return obj.medicines.count()
    
    def validate_name(self, value):
        """Validate and format supplier name."""
        if not value or not value.strip():
            raise serializers.ValidationError("Supplier name cannot be empty.")
        return ' '.join(word.capitalize() for word in value.strip().split())
    
    def validate_email(self, value):
        """Normalize email and ensure it's unique."""
        value = value.lower().strip()
        if Supplier.objects.filter(email__iexact=value).exists():
            if self.instance is None or self.instance.email.lower() != value:
                raise serializers.ValidationError("A supplier with this email already exists.")
        return value
    
    def validate_phone(self, value):
        """Validate and format phone number."""
        if not value or not value.strip():
            raise serializers.ValidationError("Phone number is required.")
        
        # Remove all non-digit characters except leading +
        cleaned = ''.join(c for c in value if c == '+' or c.isdigit())
        
        # Basic validation (customize based on your needs)
        if not cleaned or len(cleaned) < 8 or len(cleaned) > 15:
            raise serializers.ValidationError("Enter a valid phone number.")
            
        return cleaned
    
    def validate_address(self, value):
        """Validate and clean address."""
        if not value or not value.strip():
            raise serializers.ValidationError("Address cannot be empty.")
        return ' '.join(value.strip().split())  # Normalize whitespace
    
    def create(self, validated_data):
        """Create a new supplier with validated data."""
        # Ensure email is lowercase
        if 'email' in validated_data:
            validated_data['email'] = validated_data['email'].lower()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update supplier with validated data."""
        # Ensure email is lowercase
        if 'email' in validated_data:
            validated_data['email'] = validated_data['email'].lower()
        return super().update(instance, validated_data)

class MedicineSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    is_expired = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    category_display = serializers.SerializerMethodField()
    
    class Meta:
        model = Medicine
        fields = [
            'id', 'name', 'description', 'category', 'category_display', 
            'quantity', 'dosage', 'expiry_date', 'threshold_alert', 
            'supplier', 'supplier_name', 'is_active', 'is_expired', 
            'is_low_stock', 'Date_Added', 'Last_Updated',
            'manufacturer', 'price', 'reorder_level'
        ]
        read_only_fields = ('Date_Added', 'Last_Updated', 'is_expired', 'is_low_stock')
        extra_kwargs = {
            'name': {
                'error_messages': {
                    'blank': 'Medicine name cannot be blank.',
                    'max_length': 'Name cannot be longer than 200 characters.'
                }
            },
            'expiry_date': {
                'error_messages': {
                    'invalid': 'Enter a valid date in YYYY-MM-DD format.'
                }
            },
            'quantity': {
                'min_value': 0,
                'error_messages': {
                    'min_value': 'Quantity cannot be negative.'
                }
            },
            'threshold_alert': {
                'min_value': 0,
                'error_messages': {
                    'min_value': 'Threshold must be a positive number.'
                }
            },
            'price': {
                'min_value': 0,
                'error_messages': {
                    'min_value': 'Price cannot be negative.'
                }
            },
            'reorder_level': {
                'min_value': 0,
                'error_messages': {
                    'min_value': 'Reorder level must be a positive number.'
                }
            }
        }
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.expiry_date < timezone.now().date()
    
    def get_is_low_stock(self, obj):
        return obj.quantity <= obj.threshold_alert
    
    def get_category_display(self, obj):
        return obj.get_category_display_name()
    
    def validate_name(self, value):
        """Ensure medicine name is properly formatted and not just whitespace."""
        if not value or not value.strip():
            raise serializers.ValidationError("Medicine name cannot be empty.")
        return value.strip()
    
    def validate_expiry_date(self, value):
        """Ensure expiry date is in the future."""
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Expiry date must be in the future.")
        return value
    
    def validate_quantity(self, value):
        """Validate quantity is not negative."""
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative.")
        return value
    
    def validate_price(self, value):
        """Validate price is not negative and has proper decimal places."""
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        # Round to 2 decimal places
        return round(float(value), 2)
    
    def validate(self, data):
        """Cross-field validation."""
        # Ensure threshold_alert is less than reorder_level if both are provided
        if 'threshold_alert' in data and 'reorder_level' in data:
            if data['threshold_alert'] >= data['reorder_level']:
                raise serializers.ValidationError({
                    'threshold_alert': 'Threshold alert must be less than reorder level.'
                })
        
        # Ensure quantity is not below zero after stock operations
        if 'quantity' in data and data['quantity'] < 0:
            raise serializers.ValidationError({
                'quantity': 'Quantity cannot be negative.'
            })
            
        return data
    
    def create(self, validated_data):
        """Create a new medicine instance with validated data."""
        # Convert batch number to uppercase
        if 'batch_number' in validated_data:
            validated_data['batch_number'] = validated_data['batch_number'].upper()
            
        # Ensure name is properly capitalized
        if 'name' in validated_data:
            validated_data['name'] = ' '.join(word.capitalize() for word in validated_data['name'].split())
            
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update medicine instance with validated data."""
        # Handle batch number update
        if 'batch_number' in validated_data:
            validated_data['batch_number'] = validated_data['batch_number'].upper()
            
        # Handle name update
        if 'name' in validated_data:
            validated_data['name'] = ' '.join(word.capitalize() for word in validated_data['name'].split())
            
        return super().update(instance, validated_data)
        if value < 0:
            raise serializers.ValidationError("Quantity cannot be negative")
        return value

# Add a helper serializer for category choices
class CategoryChoiceSerializer(serializers.Serializer):
    value = serializers.CharField()
    display_name = serializers.CharField()


class MedicineStockUpdateSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)
    action = serializers.ChoiceField(choices=['ADD', 'REMOVE'])
    reason = serializers.CharField(max_length=200, required=False)
    
    def validate(self, data):
        if data['action'] == 'REMOVE' and data['quantity'] > self.context['medicine'].quantity:
            raise serializers.ValidationError("Cannot remove more than available stock")
        return data

class InventoryLogSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(source='medicine.name', read_only=True)
    performed_by_name = serializers.CharField(source='performed_by.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    prescription_id = serializers.IntegerField(source='prescription.id', read_only=True, allow_null=True)
    
    class Meta:
        model = InventoryLog
        fields = [
            'id', 'medicine', 'medicine_name', 'action', 'action_display',
            'quantity_change', 'previous_quantity', 'new_quantity',
            'performed_by', 'performed_by_name', 'reason', 'prescription',
            'prescription_id', 'timestamp'
        ]
        read_only_fields = ('timestamp',)

class PatientSerializer(serializers.ModelSerializer):
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone', 'email', 'address', 'emergency_contact', 'emergency_phone',
            'medical_history', 'allergies', 'Date_Added', 'Last_Updated', 'age'
        ]
        read_only_fields = ('Date_Added', 'Last_Updated', 'age')
        extra_kwargs = {
            'first_name': {
                'required': True,
                'error_messages': {
                    'blank': 'First name is required.',
                    'max_length': 'First name is too long.'
                }
            },
            'last_name': {
                'required': True,
                'error_messages': {
                    'blank': 'Last name is required.',
                    'max_length': 'Last name is too long.'
                }
            },
            'date_of_birth': {
                'required': True,
                'error_messages': {
                    'required': 'Date of birth is required.',
                    'invalid': 'Enter a valid date in YYYY-MM-DD format.'
                }
            },
            'gender': {
                'required': True,
                'error_messages': {
                    'required': 'Gender is required.',
                    'invalid_choice': 'Invalid gender selection.'
                }
            },
            'phone': {
                'required': False,
                'allow_blank': True,
                'error_messages': {
                    'invalid': 'Enter a valid phone number.'
                }
            },
            'email': {
                'required': False,
                'allow_blank': True,
                'error_messages': {
                    'invalid': 'Enter a valid email address.'
                }
            },
            'emergency_contact': {
                'required': False,
                'allow_blank': True,
                'error_messages': {
                    'max_length': 'Emergency contact name is too long.'
                }
            },
            'emergency_phone': {
                'required': False,
                'allow_blank': True,
                'error_messages': {
                    'invalid': 'Enter a valid emergency phone number.'
                }
            }
        }
    
    def get_age(self, obj):
        import datetime
        today = datetime.date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
    
    def validate_first_name(self, value):
        """Validate and format first name."""
        if not value or not value.strip():
            raise serializers.ValidationError("First name is required.")
        return ' '.join(word.capitalize() for word in value.strip().split())
    
    def validate_last_name(self, value):
        """Validate and format last name."""
        if not value or not value.strip():
            raise serializers.ValidationError("Last name is required.")
        return ' '.join(word.capitalize() for word in value.strip().split())
    
    def validate_date_of_birth(self, value):
        """Validate date of birth is in the past and reasonable."""
        from datetime import date
        today = date.today()
        
        # Check if date is in the future
        if value > today:
            raise serializers.ValidationError("Date of birth cannot be in the future.")
            
        # Check if age is reasonable (e.g., not older than 120 years)
        max_age = 120
        if today.year - value.year > max_age or (
            today.year - value.year == max_age and 
            (today.month, today.day) < (value.month, value.day)
        ):
            raise serializers.ValidationError(f"Age cannot be more than {max_age} years.")
            
        return value
    
    def validate_phone(self, value):
        """Validate and format phone number if provided."""
        if not value:  # Phone is optional
            return value
            
        # Remove all non-digit characters except leading +
        cleaned = ''.join(c for c in value if c == '+' or c.isdigit())
        
        # Basic validation (customize based on your needs)
        if not cleaned or len(cleaned) < 8 or len(cleaned) > 15:
            raise serializers.ValidationError("Enter a valid phone number.")
            
        return cleaned
    
    def validate_email(self, value):
        """Normalize email if provided."""
        if value:
            value = value.lower().strip()
        return value
    
    def validate_emergency_phone(self, value):
        """Validate and format emergency phone number if provided."""
        if not value:  # Emergency phone is optional
            return value
            
        # Remove all non-digit characters except leading +
        cleaned = ''.join(c for c in value if c == '+' or c.isdigit())
        
        # Basic validation (customize based on your needs)
        if not cleaned or len(cleaned) < 8 or len(cleaned) > 15:
            raise serializers.ValidationError("Enter a valid emergency phone number.")
            
        return cleaned
    
    def validate(self, data):
        """Cross-field validation."""
        # If emergency contact is provided, emergency phone should also be provided
        if data.get('emergency_contact') and not data.get('emergency_phone'):
            raise serializers.ValidationError({
                'emergency_phone': 'Emergency phone number is required when emergency contact is provided.'
            })
            
        # If emergency phone is provided, emergency contact should also be provided
        if data.get('emergency_phone') and not data.get('emergency_contact'):
            raise serializers.ValidationError({
                'emergency_contact': 'Emergency contact name is required when emergency phone is provided.'
            })
            
        return data
    
    def create(self, validated_data):
        """Create a new patient with validated data."""
        # Normalize email if provided
        if 'email' in validated_data and validated_data['email']:
            validated_data['email'] = validated_data['email'].lower().strip()
            
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """Update patient with validated data."""
        # Normalize email if provided
        if 'email' in validated_data and validated_data['email']:
            validated_data['email'] = validated_data['email'].lower().strip()
            
        return super().update(instance, validated_data)
