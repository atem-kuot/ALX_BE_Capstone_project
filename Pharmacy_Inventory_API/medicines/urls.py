from django.urls import path
from . import views

urlpatterns = [
    # Supplier endpoints
    path('suppliers/', views.SupplierListView.as_view(), name='supplier-list'),
    path('suppliers/<int:pk>/', views.SupplierDetailView.as_view(), name='supplier-detail'),
    
    # Medicine endpoints
    path('medicines/', views.MedicineListView.as_view(), name='medicine-list'),
    path('medicines/<int:pk>/', views.MedicineDetailView.as_view(), name='medicine-detail'),
    path('medicines/<int:pk>/update-stock/', views.update_stock, name='medicine-update-stock'),
    
    # Alert endpoints
    path('medicines/alerts/expiry/', views.medicine_expiry_alerts, name='medicine-expiry-alerts'),
    path('medicines/alerts/low-stock/', views.medicine_low_stock, name='medicine-low-stock'),

    # Inventory tracking endpoints
    path('inventory-logs/', views.InventoryLogListView.as_view(), name='inventory-log-list'),
    path('medicines/<int:pk>/inventory-history/', views.MedicineInventoryHistoryView.as_view(), name='medicine-inventory-history'),
    
    # Patient endpoints
    path('patients/', views.PatientListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', views.PatientDetailView.as_view(), name='patient-detail'),
    path('patients/<int:pk>/medication-history/', views.PatientMedicationHistoryView.as_view(), name='patient-medication-history'),

    # Search endpoints
    path('medicines/search/', views.MedicineSearchView.as_view(), name='medicine-search'),
    path('medicines/autocomplete/', views.medicine_autocomplete, name='medicine-autocomplete'),
]