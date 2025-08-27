from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db import transaction

from core.pagination import CustomPageNumberPagination
from core.permissions import IsDoctor, IsPharmacist, IsAdmin
from .models import Prescription, PrescriptionMedicine
from .serializers import (
    PrescriptionSerializer, PrescriptionStatusSerializer, 
    PrescriptionFulfillSerializer, PrescriptionMedicineCreateSerializer
)

class PrescriptionListView(generics.ListCreateAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'is_urgent', 'patient', 'prescribed_by']
    search_fields = [
        'patient__first_name', 'patient__last_name',
        'diagnosis', 'notes', 'prescribed_by__username'
    ]
    ordering_fields = [
        'date_issued', 'date_fulfilled', 'status', 'is_urgent'
    ]
    ordering = ['-date_issued']

    def get_queryset(self):
        queryset = Prescription.objects.select_related(
            'patient', 'prescribed_by', 'fulfilled_by'
        ).prefetch_related('prescription_medicines__medicine')
        
        # Doctors can only see their own prescriptions
        if self.request.user.role == 'DOCTOR':
            queryset = queryset.filter(prescribed_by=self.request.user)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(date_issued__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date_issued__date__lte=end_date)
        
        # Filter by patient name
        patient_name = self.request.query_params.get('patient_name')
        if patient_name:
            queryset = queryset.filter(
                models.Q(patient__first_name__icontains=patient_name) |
                models.Q(patient__last_name__icontains=patient_name)
            )
        
        return queryset

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsDoctor()]
        return [permissions.IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(prescribed_by=self.request.user)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PrescriptionCreateSerializer
        return PrescriptionSerializer

class PrescriptionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Prescription.objects.select_related(
        'patient', 'prescribed_by', 'fulfilled_by'
    ).prefetch_related('prescription_medicines__medicine')
    serializer_class = PrescriptionSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsDoctor() | IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PrescriptionStatusSerializer
        return PrescriptionSerializer

class PrescriptionFulfillView(generics.UpdateAPIView):
    queryset = Prescription.objects.filter(status__in=['PENDING', 'PARTIALLY_FULFILLED'])
    serializer_class = PrescriptionFulfillSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacist]

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        prescription = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        data = serializer.validated_data
        partial_fulfillment = data.get('partial', False)
        
        try:
            if partial_fulfillment:
                prescription.status = 'PARTIALLY_FULFILLED'
            else:
                # Check if all medicines can be fulfilled
                if not prescription.can_be_fulfilled():
                    return Response(
                        {'error': 'Insufficient stock for some medicines'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # Deduct stock and mark as fulfilled
                for pm in prescription.prescription_medicines.all():
                    pm.medicine.update_quantity(
                        change_amount=-pm.quantity,
                        action='PRESCRIPTION_FULFILL',
                        user=request.user,
                        reason=f'Prescription #{prescription.id} fulfillment',
                        prescription=prescription
                    )
                    pm.is_fulfilled = True
                    pm.save()
                
                prescription.status = 'FULFILLED'
                prescription.date_fulfilled = timezone.now()
            
            prescription.fulfilled_by = request.user
            if data.get('notes'):
                prescription.notes = f"{prescription.notes}\nFulfillment notes: {data['notes']}"
            
            prescription.save()
            
            return Response(PrescriptionSerializer(prescription).data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class PrescriptionCancelView(generics.UpdateAPIView):
    queryset = Prescription.objects.exclude(status='CANCELLED')
    serializer_class = PrescriptionStatusSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctor | IsAdmin]

    def update(self, request, *args, **kwargs):
        prescription = self.get_object()
        prescription.status = 'CANCELLED'
        prescription.date_cancelled = timezone.now()
        prescription.save()
        
        return Response(PrescriptionSerializer(prescription).data)

class PrescriptionMedicineView(generics.RetrieveUpdateAPIView):
    queryset = PrescriptionMedicine.objects.select_related('medicine')
    serializer_class = PrescriptionMedicineCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsPharmacist]

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def prescription_stats(request):
    """Get prescription statistics"""
    total = Prescription.objects.count()
    pending = Prescription.objects.filter(status='PENDING').count()
    fulfilled = Prescription.objects.filter(status='FULFILLED').count()
    cancelled = Prescription.objects.filter(status='CANCELLED').count()
    urgent = Prescription.objects.filter(is_urgent=True, status='PENDING').count()
    
    return Response({
        'total': total,
        'pending': pending,
        'fulfilled': fulfilled,
        'cancelled': cancelled,
        'urgent_pending': urgent
    })