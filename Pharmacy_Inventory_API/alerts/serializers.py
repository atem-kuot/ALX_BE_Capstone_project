from rest_framework import serializers
from .models import AlertLog, AlertPreference
from medicines.serializers import MedicineSerializer
from prescriptions.serializers import PrescriptionSerializer
from core.serializers import UserSerializer

class AlertLogSerializer(serializers.ModelSerializer):
    medicine_details = MedicineSerializer(source='medicine', read_only=True)
    prescription_details = PrescriptionSerializer(source='prescription', read_only=True)
    created_by_details = UserSerializer(source='user', read_only=True)
    resolved_by_details = UserSerializer(source='resolved_by', read_only=True)
    alert_type_display = serializers.CharField(source='get_alert_type_display', read_only=True)
    severity_display = serializers.CharField(source='get_severity_display', read_only=True)
    
    class Meta:
        model = AlertLog
        fields = [
            'id', 'alert_type', 'alert_type_display', 'severity', 'severity_display',
            'title', 'message', 'medicine', 'medicine_details', 'prescription',
            'prescription_details', 'user', 'created_by_details', 'is_resolved',
            'resolved_by', 'resolved_by_details', 'resolved_at', 'resolved_notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class AlertResolveSerializer(serializers.Serializer):
    resolved_notes = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Notes about how the alert was resolved"
    )

class AlertPreferenceSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = AlertPreference
        fields = [
            'id', 'user', 'user_details', 'email_notifications', 'push_notifications',
            'sms_notifications', 'receive_low_stock_alerts', 'receive_expiry_alerts',
            'receive_prescription_alerts', 'receive_system_alerts', 'min_severity_level',
            'daily_digest', 'immediate_alerts', 'updated_at'
        ]
        read_only_fields = ['user', 'updated_at']

class AlertStatsSerializer(serializers.Serializer):
    total_alerts = serializers.IntegerField()
    unresolved_alerts = serializers.IntegerField()
    critical_alerts = serializers.IntegerField()
    high_alerts = serializers.IntegerField()
    medium_alerts = serializers.IntegerField()
    low_alerts = serializers.IntegerField()
    alerts_by_type = serializers.DictField()