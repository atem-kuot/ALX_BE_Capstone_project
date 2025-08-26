from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from .models import Medicine, Supplier
from core.pagination import CustomPageNumberPagination
from .serializers import MedicineSerializer, SupplierSerializer, MedicineStockUpdateSerializer
from core.permissions import IsAdmin, IsPharmacist
from rest_framework import generics, filters
from .models import InventoryLog, Patient
from .serializers import InventoryLogSerializer, PatientSerializer

class SupplierListView(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'Date_Added']
    ordering = ['name']

class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = CustomPageNumberPagination

class MedicineListView(generics.ListCreateAPIView):
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'supplier', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'quantity', 'expiry_date', 'created_at', 'updated_at',
        'category', 'dosage']
    ordering = ['name']  # Default ordering

    def get_queryset(self):
        queryset = Medicine.objects.select_related('supplier')
        
        # Filter by expiry status
        expiry_filter = self.request.query_params.get('expiry_status')
        if expiry_filter == 'expired':
            queryset = queryset.filter(expiry_date__lt=timezone.now().date())
        elif expiry_filter == 'not_expired':
            queryset = queryset.filter(expiry_date__gte=timezone.now().date())
        
        # Filter by stock status
        stock_filter = self.request.query_params.get('stock_status')
        if stock_filter == 'low':
            queryset = queryset.filter(quantity__lte=F('threshold_alert'))
        elif stock_filter == 'adequate':
            queryset = queryset.filter(quantity__gt=F('threshold_alert'))
        
        return queryset
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdmin() or IsPharmacist()]
        return [permissions.IsAuthenticated()]

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    
    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated(), IsAdmin() or IsPharmacist()]
        return [permissions.IsAuthenticated()]

class MedicineSearchView(generics.ListAPIView):
    """Search medicines by name for prescription creation"""
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # No pagination for search dropdowns
    
    def get_queryset(self):
        search_term = self.request.query_params.get('search', '')
        category = self.request.query_params.get('category', '')
        
        queryset = Medicine.objects.filter(is_active=True)
        
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        
        if category:
            queryset = queryset.filter(category=category)
        
        # Only show medicines with positive stock
        queryset = queryset.filter(quantity__gt=0)
        
        return queryset.order_by('name')[:20]  # Limit to 20 results

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicine_autocomplete(request):
    """Quick autocomplete for medicine names"""
    search_term = request.GET.get('search', '')
    
    if not search_term or len(search_term) < 2:
        return Response([])
    
    medicines = Medicine.objects.filter(
        name__icontains=search_term,
        is_active=True,
        quantity__gt=0
    ).values('id', 'name', 'dosage', 'quantity')[:10]
    
    return Response([
        {
            'id': med['id'],
            'label': f"{med['name']} ({med['dosage']}) - {med['quantity']} in stock",
            'name': med['name'],
            'dosage': med['dosage'],
            'quantity': med['quantity']
        }
        for med in medicines
    ])


class InventoryLogListView(generics.ListAPIView):
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medicine', 'action', 'performed_by']
    ordering_fields = ['timestamp', 'quantity_change']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        queryset = InventoryLog.objects.select_related(
            'medicine', 'performed_by', 'prescription'
        )
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
        
        return queryset

class MedicineInventoryHistoryView(generics.ListAPIView):
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        medicine_id = self.kwargs['pk']
        return InventoryLog.objects.filter(
            medicine_id=medicine_id
        ).select_related('performed_by', 'prescription').order_by('-timestamp')

class PatientListView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['last_name', 'first_name', 'date_of_birth', 
        'created_at', 'updated_at']
    ordering = ['first_name', 'last_name']  # Default ordering

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination

class PatientMedicationHistoryView(generics.ListAPIView):
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        patient_id = self.kwargs['pk']
        return InventoryLog.objects.filter(
            prescription__patient_id=patient_id,
            action='PRESCRIPTION_FULFILL'
        ).select_related('medicine', 'performed_by', 'prescription').order_by('-timestamp')



@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicine_expiry_alerts(request):
    threshold_days = int(request.query_params.get('days', 30))
    alert_date = timezone.now().date() + timezone.timedelta(days=threshold_days)
    
    medicines = Medicine.objects.filter(
        expiry_date__lte=alert_date,
        expiry_date__gte=timezone.now().date()
    )
    
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicine_low_stock(request):
    medicines = Medicine.objects.filter(quantity__lte=F('threshold_alert'))
    serializer = MedicineSerializer(medicines, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsPharmacist | IsAdmin])
def update_stock(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    serializer = MedicineStockUpdateSerializer(data=request.data, context={'medicine': medicine})
    
    if serializer.is_valid():
        data = serializer.validated_data
        try:
            if data['action'] == 'ADD':
                medicine.update_quantity(
                    change_amount=data['quantity'],
                    action='STOCK_ADD',
                    user=request.user,
                    reason=data.get('reason', 'Manual stock addition')
                )
            else:
                medicine.update_quantity(
                    change_amount=-data['quantity'],
                    action='STOCK_REMOVE',
                    user=request.user,
                    reason=data.get('reason', 'Manual stock removal')
                )
            
            return Response(MedicineSerializer(medicine).data)
            
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


