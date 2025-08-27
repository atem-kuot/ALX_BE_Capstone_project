from rest_framework import serializers
from django.db import transaction
from .models import Prescription, PrescriptionMedicine
from medicines.serializers import MedicineSerializer, PatientSerializer

class PrescriptionMedicineCreateSerializer(serializers.ModelSerializer):
    medicine_name = serializers.CharField(write_only=True)
    medicine_id = serializers.IntegerField(required=False)
    
    class Meta:
        model = PrescriptionMedicine
        fields = [
            'medicine_name', 'medicine_id', 'quantity', 
            'dosage_instructions', 'duration'
        ]
    
    def validate(self, data):
        medicine_name = data.get('medicine_name')
        medicine_id = data.get('medicine_id')
        
        if not medicine_id and not medicine_name:
            raise serializers.ValidationError("Either medicine_id or medicine_name is required")
        
        # If medicine_name is provided, try to find the medicine
        if medicine_name and not medicine_id:
            try:
                # Look for exact match first, then partial
                medicine = Medicine.objects.get(
                    name__iexact=medicine_name,
                    is_active=True
                )
                data['medicine_id'] = medicine.id
            except Medicine.DoesNotExist:
                # Try partial match
                medicines = Medicine.objects.filter(
                    name__icontains=medicine_name,
                    is_active=True
                )
                if medicines.count() == 1:
                    data['medicine_id'] = medicines.first().id
                else:
                    raise serializers.ValidationError(
                        f"Medicine '{medicine_name}' not found or multiple matches found. "
                        f"Please use medicine_id for precise selection."
                    )
        
        return data

class PrescriptionCreateSerializer(serializers.ModelSerializer):
    patient_id = serializers.IntegerField(write_only=True)
    medicines = PrescriptionMedicineCreateSerializer(many=True)
    
    class Meta:
        model = Prescription
        fields = [
            'patient_id', 'diagnosis', 'notes', 'is_urgent', 'medicines'
        ]
    
    def create(self, validated_data):
        medicines_data = validated_data.pop('medicines', [])
        
        with transaction.atomic():
            prescription = Prescription.objects.create(
                **validated_data,
                prescribed_by=self.context['request'].user
            )
            
            for medicine_data in medicines_data:
                PrescriptionMedicine.objects.create(
                    prescription=prescription,
                    medicine_id=medicine_data['medicine_id'],
                    quantity=medicine_data['quantity'],
                    dosage_instructions=medicine_data.get('dosage_instructions', ''),
                    duration=medicine_data.get('duration', '')
                )
        
        return prescription


class PrescriptionSerializer(serializers.ModelSerializer):
    patient_details = PatientSerializer(source='patient', read_only=True)
    patient_id = serializers.IntegerField(write_only=True)
    prescribed_by_name = serializers.CharField(source='prescribed_by.get_full_name', read_only=True)
    fulfilled_by_name = serializers.CharField(source='fulfilled_by.get_full_name', read_only=True)
    medicines = MedicineSerializer(many=True, source='medicines')
    total_medicines = serializers.IntegerField(read_only=True)
    can_be_fulfilled = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'patient_id', 'patient_details', 'prescribed_by', 'prescribed_by_name',
            'fulfilled_by', 'fulfilled_by_name', 'status', 'diagnosis', 'notes',
            'is_urgent', 'date_issued', 'date_fulfilled', 'date_cancelled',
            'medicines', 'total_medicines', 'can_be_fulfilled'
        ]
        read_only_fields = [
            'prescribed_by', 'fulfilled_by', 'date_issued', 
            'date_fulfilled', 'date_cancelled'
        ]

    def create(self, validated_data):
        medicines_data = validated_data.pop('prescription_medicines', [])
        
        with transaction.atomic():
            prescription = Prescription.objects.create(
                **validated_data,
                prescribed_by=self.context['request'].user
            )
            
            for medicine_data in medicines_data:
                PrescriptionMedicine.objects.create(
                    prescription=prescription,
                    medicine_id=medicine_data['medicine_id'],
                    quantity=medicine_data['quantity'],
                    dosage_instructions=medicine_data.get('dosage_instructions', ''),
                    duration=medicine_data.get('duration', '')
                )
        
        return prescription

    def update(self, instance, validated_data):
        medicines_data = validated_data.pop('prescription_medicines', None)
        
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            
            if medicines_data is not None:
                # Clear existing medicines and add new ones
                instance.prescription_medicines.all().delete()
                for medicine_data in medicines_data:
                    PrescriptionMedicine.objects.create(
                        prescription=instance,
                        medicine_id=medicine_data['medicine_id'],
                        quantity=medicine_data['quantity'],
                        dosage_instructions=medicine_data.get('dosage_instructions', ''),
                        duration=medicine_data.get('duration', '')
                    )
        
        return instance

class PrescriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = ['status', 'notes']

class PrescriptionFulfillSerializer(serializers.Serializer):
    partial = serializers.BooleanField(default=False)
    notes = serializers.CharField(required=False, allow_blank=True)