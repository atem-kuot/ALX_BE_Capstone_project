from django.contrib import admin
from .models import Medicine, Supplier

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact_person', 'email', 'phone', 'medicine_count')
    list_filter = ('Date_Added',)
    search_fields = ('name', 'contact_person', 'email')
    
    def medicine_count(self, obj):
        return obj.medicines.count()
    medicine_count.short_description = 'Medicines'

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'quantity', 'dosage', 'expiry_date', 'supplier', 'is_active')
    list_filter = ('category', 'is_active', 'expiry_date', 'supplier')
    search_fields = ('name', 'description')
    readonly_fields = ('Date_Added', 'Last_Updated')
    list_editable = ('quantity', 'is_active')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'category', 'dosage')
        }),
        ('Inventory', {
            'fields': ('quantity', 'threshold_alert', 'expiry_date', 'supplier')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('Date_Added', 'Last_Updated'),
            'classes': ('collapse',)
        })
    )