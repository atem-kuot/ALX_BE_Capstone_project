from django.contrib import admin
from .models import Prescription, PrescriptionMedicine

class PrescriptionMedicineInline(admin.TabularInline):
    model = PrescriptionMedicine
    extra = 1
    readonly_fields = ['is_fulfilled']
    fields = ['medicine', 'quantity', 'dosage_instructions', 'duration', 'is_fulfilled']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['id', 'patient', 'prescribed_by', 'status', 'is_urgent', 'date_issued']
    list_filter = ['status', 'is_urgent', 'date_issued', 'prescribed_by']
    search_fields = ['patient__first_name', 'patient__last_name', 'diagnosis']
    readonly_fields = ['date_issued', 'date_fulfilled', 'date_cancelled']
    inlines = [PrescriptionMedicineInline]
    
    fieldsets = (
        ('Patient Information', {
            'fields': ('patient', 'prescribed_by', 'fulfilled_by')
        }),
        ('Prescription Details', {
            'fields': ('status', 'diagnosis', 'notes', 'is_urgent')
        }),
        ('Timestamps', {
            'fields': ('date_issued', 'date_fulfilled', 'date_cancelled'),
            'classes': ('collapse',)
        })
    )

@admin.register(PrescriptionMedicine)
class PrescriptionMedicineAdmin(admin.ModelAdmin):
    list_display = ['prescription', 'medicine', 'quantity', 'is_fulfilled']
    list_filter = ['is_fulfilled', 'prescription__status']
    search_fields = ['medicine__name', 'prescription__patient__first_name']