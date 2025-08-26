from django.urls import path
from . import views

urlpatterns = [
    path('prescriptions/', views.PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/<int:pk>/', views.PrescriptionDetailView.as_view(), name='prescription-detail'),
    path('prescriptions/<int:pk>/fulfill/', views.PrescriptionFulfillView.as_view(), name='prescription-fulfill'),
    path('prescriptions/<int:pk>/cancel/', views.PrescriptionCancelView.as_view(), name='prescription-cancel'),
    path('prescriptions/medicines/<int:pk>/', views.PrescriptionMedicineView.as_view(), name='prescription-medicine-detail'),
    path('prescriptions/stats/', views.prescription_stats, name='prescription-stats'),
]