from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404

from core.pagination import CustomPageNumberPagination
from core.permissions import IsPharmacist, IsAdmin
from .models import AlertLog, AlertPreference
from .serializers import (
    AlertLogSerializer, AlertResolveSerializer, 
    AlertPreferenceSerializer, AlertStatsSerializer
)

class AlertListView(generics.ListAPIView):
    serializer_class = AlertLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['alert_type', 'severity', 'is_resolved', 'medicine']
    search_fields = ['title', 'message', 'medicine__name']
    ordering_fields = ['created_at', 'severity', 'alert_type']
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = AlertLog.objects.select_related(
            'medicine', 'prescription', 'user', 'resolved_by'
        )
        
        # Filter by resolved status
        resolved = self.request.query_params.get('resolved')
        if resolved == 'true':
            queryset = queryset.filter(is_resolved=True)
        elif resolved == 'false':
            queryset = queryset.filter(is_resolved=False)
        
        # Filter by severity
        severity = self.request.query_params.get('severity')
        if severity:
            queryset = queryset.filter(severity=severity)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(created_at__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__date__lte=end_date)
        
        # Pharmacists and admins see all alerts, others see only their relevant ones
        if self.request.user.role not in ['PHARMACIST', 'ADMIN']:
            queryset = queryset.filter(
                Q(user=self.request.user) |
                Q(prescription__prescribed_by=self.request.user) |
                Q(severity__in=['CRITICAL', 'HIGH'])
            )
        
        return queryset

class AlertDetailView(generics.RetrieveAPIView):
    queryset = AlertLog.objects.select_related(
        'medicine', 'prescription', 'user', 'resolved_by'
    )
    serializer_class = AlertLogSerializer
    permission_classes = [permissions.IsAuthenticated]

class AlertResolveView(generics.UpdateAPIView):
    queryset = AlertLog.objects.filter(is_resolved=False)
    serializer_class = AlertResolveSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacist | IsAdmin]

    def update(self, request, *args, **kwargs):
        alert = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        alert.resolve(
            user=request.user,
            notes=serializer.validated_data.get('resolved_notes', '')
        )
        
        return Response(AlertLogSerializer(alert).data)

class AlertPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = AlertPreferenceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Get or create preferences for the current user
        obj, created = AlertPreference.objects.get_or_create(user=self.request.user)
        return obj

class UnresolvedAlertsView(generics.ListAPIView):
    serializer_class = AlertLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # Typically want to see all unresolved alerts

    def get_queryset(self):
        return AlertLog.objects.filter(
            is_resolved=False
        ).select_related('medicine', 'prescription').order_by('-severity', '-created_at')

class CriticalAlertsView(generics.ListAPIView):
    serializer_class = AlertLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None

    def get_queryset(self):
        return AlertLog.objects.filter(
            is_resolved=False,
            severity__in=['CRITICAL', 'HIGH']
        ).select_related('medicine', 'prescription').order_by('-created_at')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def alert_stats(request):
    """Get alert statistics"""
    total_alerts = AlertLog.objects.count()
    unresolved_alerts = AlertLog.objects.filter(is_resolved=False).count()
    
    severity_counts = AlertLog.objects.filter(is_resolved=False).values(
        'severity'
    ).annotate(count=Count('id'))
    
    type_counts = AlertLog.objects.filter(is_resolved=False).values(
        'alert_type'
    ).annotate(count=Count('id'))
    
    stats = {
        'total_alerts': total_alerts,
        'unresolved_alerts': unresolved_alerts,
        'critical_alerts': next((item['count'] for item in severity_counts if item['severity'] == 'CRITICAL'), 0),
        'high_alerts': next((item['count'] for item in severity_counts if item['severity'] == 'HIGH'), 0),
        'medium_alerts': next((item['count'] for item in severity_counts if item['severity'] == 'MEDIUM'), 0),
        'low_alerts': next((item['count'] for item in severity_counts if item['severity'] == 'LOW'), 0),
        'alerts_by_type': {item['alert_type']: item['count'] for item in type_counts}
    }
    
    return Response(stats)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsAdmin])
def bulk_resolve_alerts(request):
    """Resolve multiple alerts at once"""
    alert_ids = request.data.get('alert_ids', [])
    notes = request.data.get('notes', '')
    
    if not alert_ids:
        return Response(
            {'error': 'No alert IDs provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    alerts = AlertLog.objects.filter(id__in=alert_ids, is_resolved=False)
    resolved_count = 0
    
    for alert in alerts:
        alert.resolve(request.user, notes)
        resolved_count += 1
    
    return Response({
        'message': f'Resolved {resolved_count} alerts',
        'resolved_count': resolved_count
    })

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
import json

@api_view(['POST'])
@permission_classes([])  # No authentication for Telegram webhook
def telegram_webhook(request):
    """
    Handle incoming Telegram webhook messages
    """
    try:
        data = json.loads(request.body)
        message = data.get('message', {})
        text = message.get('text', '').strip()
        chat_id = message.get('chat', {}).get('id')
        
        if text == '/start':
            response_text = "🤖 Pharmacy Alert Bot Activated!\n\n"
            response_text += "Available commands:\n"
            response_text += "/alerts - Show unresolved alerts\n"
            response_text += "/stats - Show alert statistics\n"
            response_text += "/help - Show this help message"
            
            send_telegram_message(chat_id, response_text)
            
        elif text == '/alerts':
            from .models import AlertLog
            alerts = AlertLog.objects.filter(is_resolved=False)[:5]
            
            if alerts:
                response_text = "🚨 Unresolved Alerts:\n\n"
                for alert in alerts:
                    response_text += f"• {alert.title}\n"
                response_text += "\nView all alerts in the system."
            else:
                response_text = "✅ No unresolved alerts!"
                
            send_telegram_message(chat_id, response_text)
            
        elif text == '/stats':
            from .models import AlertLog
            stats = AlertLog.objects.aggregate(
                total=Count('id'),
                unresolved=Count('id', filter=Q(is_resolved=False)),
                critical=Count('id', filter=Q(severity='CRITICAL', is_resolved=False))
            )
            
            response_text = f"""
📊 Alert Statistics:
Total: {stats['total']}
Unresolved: {stats['unresolved']}
Critical: {stats['critical']}
            """.strip()
            
            send_telegram_message(chat_id, response_text)
            
        elif text == '/help':
            response_text = "🤖 Pharmacy Alert Bot Help\n\n"
            response_text += "Commands:\n"
            response_text += "/start - Start the bot\n"
            response_text += "/alerts - Show recent alerts\n"
            response_text += "/stats - Show statistics\n"
            response_text += "/help - This message"
            
            send_telegram_message(chat_id, response_text)
        
        return Response({'status': 'ok'})
        
    except Exception as e:
        logger.error(f"Telegram webhook error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

def send_telegram_message(chat_id, text):
    """Helper function to send message to specific chat"""
    from core.telegram_service import TelegramBotService
    service = TelegramBotService()
    service.send_message(text, chat_id=chat_id)