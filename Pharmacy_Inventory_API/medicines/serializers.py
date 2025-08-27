from rest_framework import serializers
from .models import Medicine, Supplier
from rest_framework import serializers
from .models import Medicine, Supplier, InventoryLog, Patient
from prescriptions.models import Prescription

class SupplierSerializer(serializers.ModelSerializer):
    medicine_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Supplier
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
    
    def get_medicine_count(self, obj):
        return obj.medicines.count()

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
            'is_low_stock', 'Date_Added', 'Last_Updated'
        ]
        read_only_fields = ('Date_Added', 'Last_Updated')
    
    def get_is_expired(self, obj):
        from django.utils import timezone
        return obj.expiry_date < timezone.now().date()
    
    def get_is_low_stock(self, obj):
        return obj.quantity <= obj.threshold_alert
    
    def get_category_display(self, obj):
        return obj.get_category_display_name()
    
    def validate_expiry_date(self, value):
        from django.utils import timezone
        if value <= timezone.now().date():
            raise serializers.ValidationError("Expiry date must be in the future")
        return value
    
    def validate_quantity(self, value):
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
            'id', 'first_name', 'last_name', 'date_of_birth', 'age',
            'gender', 'phone', 'email', 'address', 'emergency_contact',
            'emergency_phone', 'medical_history', 'allergies',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - (
            (today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day)
        )
