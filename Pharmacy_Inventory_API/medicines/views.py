from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Q, F
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from .models import Medicine, Supplier
from core.pagination import CustomPageNumberPagination
from .serializers import MedicineSerializer, SupplierSerializer, MedicineStockUpdateSerializer
from core.permissions import IsAdmin, IsPharmacist
from rest_framework import generics, filters
from .models import InventoryLog, Patient
from .serializers import InventoryLogSerializer, PatientSerializer

class SupplierListView(generics.ListCreateAPIView):
    """
    API endpoint that allows suppliers to be viewed or created.
    
    ### Permissions:
    - User must be authenticated and have admin privileges
    
    ### Query Parameters:
    - `search` (string): Search by name, contact person, or email
    - `ordering` (string): Order by any field. Prefix with '-' for descending order
    - `page` (int): Page number for pagination
    - `page_size` (int): Number of results per page
    
    ### Example Requests:
    - GET /api/suppliers/?search=pharma&ordering=-date_added
    - POST /api/suppliers/ with supplier data in request body
    """
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'contact_person', 'email']
    ordering_fields = ['name', 'Date_Added']
    ordering = ['name']
    
    def get_queryset(self):
        """
        Return a queryset of suppliers with only the necessary fields.
        Optimized to reduce database load by selecting specific fields.
        """
        return Supplier.objects.all().only('id', 'name', 'contact_person', 'email', 'phone', 'Date_Added')
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - GET: Any authenticated user can view
        - POST: Only admin or pharmacist can create
        """
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        # For POST, check if user is either admin or pharmacist
        if self.request.user.role in ['ADMIN', 'PHARMACIST']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]  # This will deny access

class SupplierDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows viewing, updating, or deleting a supplier.
    
    ### Permissions:
    - User must be authenticated and have admin privileges
    
    ### Allowed Methods:
    - GET: Retrieve supplier details
    - PUT: Update all supplier fields
    - PATCH: Partially update supplier fields
    - DELETE: Remove the supplier (soft delete)
    
    ### Example Requests:
    - GET /api/suppliers/1/
    - PUT /api/suppliers/1/ with updated supplier data
    - DELETE /api/suppliers/1/
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """Return a queryset that includes related fields efficiently."""
        return Supplier.objects.select_related('created_by').only(
            'id', 'name', 'contact_person', 'email', 'phone', 'address',
            'tax_id', 'notes', 'created_at', 'updated_at', 'created_by_id',
            'is_active'
        )

class MedicineListView(generics.ListCreateAPIView):
    """
    API endpoint that allows medicines to be viewed or created.
    
    ### Permissions:
    - User must be authenticated to view (GET)
    - User must be admin or pharmacist to create (POST)
    
    ### Query Parameters:
    - `search` (string): Search by name or description
    - `category` (string): Filter by category
    - `supplier` (int): Filter by supplier ID
    - `is_active` (bool): Filter active/inactive medicines
    - `stock_status` (string): 'low' or 'adequate'
    - `expiry_status` (string): 'expired' or 'not_expired'
    - `ordering` (string): Order by any field. Prefix with '-' for descending
    - `page` (int): Page number for pagination
    - `page_size` (int): Number of results per page
    
    ### Example Requests:
    - GET /api/medicines/?search=aspirin&category=pain&stock_status=low
    - POST /api/medicines/ with medicine data in request body
    """
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'supplier', 'is_active']
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'quantity', 'expiry_date', 'created_at', 'updated_at',
        'category', 'dosage', 'price']
    ordering = ['name']  # Default ordering
    
    # Only select necessary fields for better performance
    select_related_fields = ['supplier']
    only_fields = [
        'id', 'name', 'description', 'category', 'quantity', 'dosage',
        'expiry_date', 'threshold_alert', 'supplier', 'is_active',
        'batch_number', 'manufacturer', 'price', 'reorder_level',
        'created_at', 'updated_at'
    ]

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
            # For POST requests, check if user is either admin or pharmacist
            if self.request.user.role in ['ADMIN', 'PHARMACIST']:
                return [permissions.IsAuthenticated()]
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]  # This will deny access
        return [permissions.IsAuthenticated()]

class MedicineDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows viewing, updating, or deleting a medicine.
    
    ### Permissions:
    - User must be authenticated to view (GET)
    - User must be admin/pharmacist to update/delete (PUT/PATCH/DELETE)
    
    ### Allowed Methods:
    - GET: Retrieve medicine details
    - PUT: Update all medicine fields
    - PATCH: Partially update medicine fields
    - DELETE: Remove the medicine (soft delete)
    
    ### Example Requests:
    - GET /api/medicines/1/
    - PATCH /api/medicines/1/ with partial update data
    - DELETE /api/medicines/1/
    """
    serializer_class = MedicineSerializer
    lookup_field = 'pk'
    
    def get_queryset(self):
        """Return a queryset that includes related fields efficiently."""
        return Medicine.objects.select_related('supplier').only(
            'id', 'name', 'description', 'category', 'quantity', 'dosage',
            'expiry_date', 'threshold_alert', 'supplier_id', 'is_active',
            'batch_number', 'manufacturer', 'price', 'reorder_level',
            'created_at', 'updated_at', 'created_by_id'
        )
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        - GET: Any authenticated user can view
        - PUT/PATCH/DELETE: Only ADMIN or PHARMACIST can update/delete
        """
        if self.request.method == 'GET':
            return [permissions.IsAuthenticated()]
        # For PUT/PATCH/DELETE, check if user is either admin or pharmacist
        if self.request.user.role in ['ADMIN', 'PHARMACIST']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), permissions.IsAdminUser()]  # This will deny access

class MedicineSearchView(generics.ListAPIView):
    """
    API endpoint for searching medicines with autocomplete functionality.
    
    This endpoint is optimized for quick search operations and is typically used
    in autocomplete dropdowns or search-as-you-type interfaces.
    
    ### Permissions:
    - User must be authenticated
    
    ### Query Parameters:
    - `search` (string): Search term to filter medicines by name or description
    - `category` (string): Optional category filter
    
    ### Response:
    Returns a list of matching medicines with basic information.
    Limited to 20 results for performance.
    
    ### Example Requests:
    - GET /api/medicines/search/?search=asp
    - GET /api/medicines/search/?search=para&category=pain
    """
    serializer_class = MedicineSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = None  # No pagination for search dropdowns
    
    def get_queryset(self):
        """
        Return a filtered queryset of active, in-stock medicines matching the search criteria.
        Optimized for performance by selecting only necessary fields and limiting results.
        """
        search_term = self.request.query_params.get('search', '').strip()
        category = self.request.query_params.get('category', '').strip()
        
        # Start with a base queryset that only selects necessary fields
        queryset = Medicine.objects.filter(
            is_active=True,
            quantity__gt=0  # Only show in-stock items
        ).select_related('supplier').only(
            'id', 'name', 'description', 'category', 'quantity', 
            'dosage', 'supplier_id', 'price', 'batch_number', 'manufacturer'
        )
        
        # Add search term filtering if provided
        if search_term:
            queryset = queryset.filter(
                Q(name__icontains=search_term) |
                Q(description__icontains=search_term)
            )
        
        # Add category filtering if provided
        if category:
            queryset = queryset.filter(category=category)
        
        return queryset.order_by('name')[:20]  # Limit to 20 results

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicine_autocomplete(request):
    """
    Lightweight autocomplete endpoint for medicine names.
    
    This endpoint is optimized for frontend autocomplete components, providing
    minimal but essential data with very low latency.
    
    ### Permissions:
    - User must be authenticated
    
    ### Query Parameters:
    - `search` (string, required): Search term (minimum 2 characters)
    
    ### Response:
    Returns a list of matching medicines with formatted labels for display.
    Limited to 10 results for performance.
    
    ### Example Requests:
    - GET /api/medicines/autocomplete/?search=asp
    
    ### Performance Notes:
    - Uses values() instead of full model instances
    - Has a minimum search term length of 2 characters
    - Returns only essential fields
    - Limited to 10 results
    """
    search_term = request.GET.get('search', '').strip()
    
    # Return early for empty or very short search terms
    if not search_term or len(search_term) < 2:
        return Response([])
    
    # Use values() to only fetch required fields
    medicines = Medicine.objects.filter(
        name__icontains=search_term,
        is_active=True,
        quantity__gt=0
    ).values(
        'id', 'name', 'dosage', 'quantity', 'price', 'batch_number'
    ).order_by('name')[:10]  # Limit to 10 results
    
    # Format response data
    response_data = [
        {
            'id': med['id'],
            'label': f"{med['name']} ({med['dosage']}) - {med['quantity']} in stock",
            'name': med['name'],
            'dosage': med['dosage'],
            'quantity': med['quantity'],
            'price': str(med['price']),
            'batch_number': med['batch_number']
        }
        for med in medicines
    ]
    
    return Response(response_data)


class InventoryLogListView(generics.ListAPIView):
    """
    API endpoint that provides access to the inventory audit log.
    
    This endpoint allows viewing a history of all inventory changes with detailed
    information about each transaction.
    
    ### Permissions:
    - User must be authenticated
    
    ### Query Parameters:
    - `action` (string): Filter by action type (e.g., 'STOCK_ADD', 'STOCK_REMOVE')
    - `medicine` (int): Filter by medicine ID
    - `performed_by` (int): Filter by user ID who performed the action
    - `start_date` (date): Filter logs after this date (YYYY-MM-DD)
    - `end_date` (date): Filter logs before this date (YYYY-MM-DD)
    - `ordering` (string): Order by any field. Prefix with '-' for descending
    - `page` (int): Page number for pagination
    - `page_size` (int): Number of results per page
    
    ### Example Requests:
    - GET /api/inventory-logs/?action=STOCK_ADD&ordering=-timestamp
    - GET /api/inventory-logs/?medicine=1&start_date=2023-01-01
    """
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['medicine', 'action', 'performed_by']
    ordering_fields = ['timestamp', 'quantity_change']
    ordering = ['-timestamp']
    
    def get_queryset(self):
        """
        Return a filtered queryset of inventory logs with related fields.
        Optimized to reduce database queries and select only necessary fields.
        """
        queryset = InventoryLog.objects.select_related(
            'medicine', 'performed_by', 'prescription'
        ).only(
            'id', 'action', 'quantity_change', 'previous_quantity',
            'new_quantity', 'timestamp', 'reason', 'medicine_id',
            'performed_by_id', 'performed_by__username', 'prescription_id'
        )
        
        # Filter by date range if provided
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
        
        return queryset

class MedicineInventoryHistoryView(generics.ListAPIView):
    """
    API endpoint that provides the inventory history for a specific medicine.
    
    This endpoint shows all inventory transactions related to a specific medicine,
    including stock additions, removals, and adjustments.
    
    ### Permissions:
    - User must be authenticated
    
    ### URL Parameters:
    - `pk` (int): The ID of the medicine to get history for
    
    ### Query Parameters:
    - `action` (string): Filter by action type
    - `start_date` (date): Filter logs after this date (YYYY-MM-DD)
    - `end_date` (date): Filter logs before this date (YYYY-MM-DD)
    - `ordering` (string): Order by any field. Default is '-timestamp'
    - `page` (int): Page number for pagination
    - `page_size` (int): Number of results per page
    
    ### Example Requests:
    - GET /api/medicines/1/history/
    - GET /api/medicines/1/history/?action=STOCK_ADD&start_date=2023-01-01
    """
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """
        Return a filtered queryset of inventory logs for the specified medicine.
        Includes related user and prescription data for context.
        """
        medicine_id = self.kwargs['pk']
        queryset = InventoryLog.objects.filter(
            medicine_id=medicine_id
        ).select_related('performed_by', 'prescription', 'medicine')
        
        # Apply additional filters if provided
        action = self.request.query_params.get('action')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        
        if action:
            queryset = queryset.filter(action=action)
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
            
        return queryset.order_by('-timestamp')

class PatientListView(generics.ListCreateAPIView):
    """
    API endpoint that allows patients to be viewed or created.
    
    This endpoint provides a searchable and sortable list of patients
    with their basic information.
    
    ### Permissions:
    - User must be authenticated
    - Only admin/pharmacist can create new patients (POST)
    
    ### Query Parameters:
    - `search` (string): Search by first name, last name, phone, or email
    - `ordering` (string): Order by any field. Prefix with '-' for descending
    - `page` (int): Page number for pagination
    - `page_size` (int): Number of results per page
    
    ### Example Requests:
    - GET /api/patients/?search=john&ordering=-created_at
    - POST /api/patients/ with patient data in request body
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['first_name', 'last_name', 'phone', 'email']
    ordering_fields = ['last_name', 'first_name', 'date_of_birth', 
        'created_at', 'updated_at']
    ordering = ['last_name', 'first_name']  # Default ordering
    
    def get_queryset(self):
        """
        Return a queryset of patients with optimized field selection.
        Only includes active patients by default.
        """
        return Patient.objects.filter(
            is_active=True
        ).only(
            'id', 'first_name', 'last_name', 'date_of_birth',
            'phone', 'email', 'address', 'created_at', 'updated_at'
        )
        
    def get_permissions(self):
        """Only allow admin/pharmacist to create new patients."""
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsAdmin() or IsPharmacist()]
        return [permissions.IsAuthenticated()]

class PatientDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API endpoint that allows viewing, updating, or deleting a patient.
    
    ### Permissions:
    - User must be authenticated to view (GET)
    - User must be admin/pharmacist to update/delete (PUT/PATCH/DELETE)
    
    ### Allowed Methods:
    - GET: Retrieve patient details
    - PUT: Update all patient fields
    - PATCH: Partially update patient fields
    - DELETE: Mark patient as inactive (soft delete)
    
    ### Example Requests:
    - GET /api/patients/1/
    - PATCH /api/patients/1/ with partial update data
    - DELETE /api/patients/1/ (soft delete)
    """
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    lookup_field = 'pk'
    
    def get_queryset(self):
        """Return a queryset that includes related fields efficiently."""
        return Patient.objects.select_related('created_by').only(
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'phone', 'email', 'address', 'city', 'state', 'postal_code',
            'insurance_provider', 'insurance_number', 'allergies', 'notes',
            'is_active', 'created_at', 'updated_at', 'created_by_id'
        )
        
    def perform_destroy(self, instance):
        """
        Override delete to perform a soft delete.
        Sets is_active=False instead of actually deleting the record.
        """
        instance.is_active = False
        instance.save(update_fields=['is_active', 'updated_at'])

class PatientMedicationHistoryView(generics.ListAPIView):
    """
    API endpoint that provides a complete medication history for a specific patient.
    
    This endpoint shows all medication-related activities for a patient,
    including prescriptions, dispensed medications, and other inventory
    transactions associated with the patient.
    
    ### Permissions:
    - User must be authenticated
    
    ### URL Parameters:
    - `pk` (int): The ID of the patient
    
    ### Query Parameters:
    - `action` (string): Filter by action type (e.g., 'DISPENSE', 'RETURN')
    - `start_date` (date): Filter logs after this date (YYYY-MM-DD)
    - `end_date` (date): Filter logs before this date (YYYY-MM-DD)
    - `medicine` (int): Filter by medicine ID
    - `page` (int): Page number for pagination
    - `page_size` (int): Number of results per page
    
    ### Example Requests:
    - GET /api/patients/1/medication-history/
    - GET /api/patients/1/medication-history/?action=DISPENSE&start_date=2023-01-01
    """
    serializer_class = InventoryLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    
    def get_queryset(self):
        """
        Return a filtered queryset of medication history for the specified patient.
        Includes related medicine, performer, and prescription data.
        """
        patient_id = self.kwargs.get('pk')
        queryset = InventoryLog.objects.select_related(
            'medicine', 'performed_by', 'prescription'
        ).filter(
            Q(prescription__patient_id=patient_id) |
            Q(patient_id=patient_id)
        )
        
        # Apply additional filters if provided
        action = self.request.query_params.get('action')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        medicine_id = self.request.query_params.get('medicine')
        
        if action:
            queryset = queryset.filter(action=action)
        if start_date:
            queryset = queryset.filter(timestamp__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(timestamp__date__lte=end_date)
        if medicine_id:
            queryset = queryset.filter(medicine_id=medicine_id)
            
        return queryset.order_by('-timestamp')

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicine_expiry_alerts(request):
    """
    API endpoint that returns a list of medicines that will expire soon.
    
    This endpoint helps identify medicines that are approaching their
    expiration date, allowing for proactive inventory management.
    
    ### Permissions:
    - User must be authenticated
    
    ### Query Parameters:
    - `days` (int, optional): Number of days to look ahead for expiring medicines. Default is 30.
    - `page` (int, optional): Page number for pagination. Default is 1.
    - `page_size` (int, optional): Number of results per page. Default is 10.
    
    ### Response:
    Returns a paginated list of medicines that will expire within the specified
    number of days, sorted by expiration date (soonest first).
    
    ### Example Requests:
    - GET /api/alerts/expiring/?days=60
    - GET /api/alerts/expiring/?days=90&page=2&page_size=20
    
    ### Performance Notes:
    - Only selects necessary fields from the database
    - Uses select_related for supplier information
    - Includes pagination to handle large result sets
    """
    # Get threshold days from query params, default to 30 days
    try:
        threshold_days = int(request.query_params.get('days', 30))
    except ValueError:
        return Response(
            {"error": "Invalid days parameter. Must be an integer."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Calculate the threshold date
    threshold_date = timezone.now().date() + timezone.timedelta(days=threshold_days)
    
    # Get pagination parameters
    page_size = request.query_params.get('page_size', 10)
    page_number = request.query_params.get('page', 1)
    
    # Get the queryset with only necessary fields
    queryset = Medicine.objects.filter(
        expiry_date__lte=threshold_date,
        expiry_date__gte=timezone.now().date(),  # Only future expiry dates
        is_active=True
    ).select_related('supplier').only(
        'id', 'name', 'description', 'quantity', 'expiry_date',
        'batch_number', 'supplier_id', 'supplier__name', 'threshold_alert'
    ).order_by('expiry_date')
    
    # Paginate the results
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    # Serialize the data
    serializer = MedicineSerializer(paginated_queryset, many=True)
    
    # Return paginated response
    return paginator.get_paginated_response(serializer.data)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def medicine_low_stock(request):
    """
    API endpoint that returns a list of medicines with low stock levels.
    
    This endpoint helps identify medicines that need to be reordered by
    checking current quantity against the threshold alert level.
    
    ### Permissions:
    - User must be authenticated
    
    ### Query Parameters:
    - `page` (int, optional): Page number for pagination. Default is 1.
    - `page_size` (int, optional): Number of results per page. Default is 10.
    
    ### Response:
    Returns a paginated list of medicines where the current quantity is less than
    or equal to the threshold alert level, sorted by quantity (lowest first).
    
    ### Example Requests:
    - GET /api/alerts/low-stock/
    - GET /api/alerts/low-stock/?page=2&page_size=20
    
    ### Performance Notes:
    - Only selects necessary fields from the database
    - Uses select_related for supplier information
    - Includes pagination to handle large result sets
    """
    # Get pagination parameters
    page_size = request.query_params.get('page_size', 10)
    page_number = request.query_params.get('page', 1)
    
    # Get the queryset with only necessary fields
    queryset = Medicine.objects.filter(
        quantity__lte=F('threshold_alert'),
        is_active=True
    ).select_related('supplier').only(
        'id', 'name', 'description', 'quantity', 'threshold_alert',
        'supplier_id', 'supplier__name', 'reorder_level',
        'batch_number', 'expiry_date'
    ).order_by('quantity')
    
    # Paginate the results
    paginator = PageNumberPagination()
    paginator.page_size = page_size
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    
    # Serialize the data
    serializer = MedicineSerializer(paginated_queryset, many=True)
    
    # Return paginated response
    return paginator.get_paginated_response(serializer.data)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated, IsPharmacist | IsAdmin])
def update_stock(request, pk):
    """
    API endpoint to update the stock level of a specific medicine.
    
    This endpoint allows authorized users (pharmacists or admins) to add or remove
    stock of a medicine and automatically creates an inventory log entry.
    
    ### Permissions:
    - User must be authenticated
    - User must be a pharmacist or admin
    
    ### URL Parameters:
    - `pk` (int): The ID of the medicine to update
    
    ### Request Body (JSON):
    ```json
    {
        "quantity_change": 10,  # Positive to add stock, negative to remove
        "reason": "RESTOCK",     # Reason for the change (e.g., 'RESTOCK', 'ADJUSTMENT')
        "notes": "Received new shipment"  # Optional notes
    }
    ```
    
    ### Response:
    - 200: Success - Returns updated medicine data
    - 400: Bad Request - Invalid input data
    - 403: Forbidden - Insufficient permissions
    - 404: Not Found - Medicine not found
    
    ### Example Requests:
    ```
    POST /api/medicines/1/update-stock/
    Content-Type: application/json
    
    {
        "quantity_change": 10,
        "reason": "RESTOCK",
        "notes": "Received new shipment"
    }
    ```
    """
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


