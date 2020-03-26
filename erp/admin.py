from django.contrib import admin
from django_countries.filters import CountryFilter

from .models import (Process, Request, HealthUnit, HealthProfessional,
                     Equipment, Manufacturer, Procurement, Supplier,
                     ProcurementDocument, DocumentType, PurchaseValidation,
                     PurchaseOrder, Stock, Warehouse, Distribution, Distributor)


class RequestInline(admin.StackedInline):
    model = Request
    extra = 1
    max_num = 1
    min_num = 1


class ProcurementInline(admin.StackedInline):
    model = Procurement
    extra = 1
    max_num = 1
    min_num = 1


class PurchaseValidationInline(admin.StackedInline):
    model = PurchaseValidation
    extra = 1
    max_num = 1
    min_num = 1


class StockInline(admin.StackedInline):
    model = Stock
    extra = 1
    max_num = 1
    min_num = 1


class ProcessAdmin(admin.ModelAdmin):
    list_display = ['code', 'creation_date']
    inlines = [
        RequestInline,
        ProcurementInline,
        PurchaseValidationInline,
        StockInline,
    ]


class RequestAdmin(admin.ModelAdmin):
    list_display = ['process', 'owner', 'health_unit', 'health_professional',
                    'equipment', 'quantity', 'maximum_available']
    list_filter = ['owner', 'health_unit', 'health_professional', 'equipment']


class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_type', 'manufacturer', 'model',
                    'manufacturer_reference']
    list_filter = ['product_type', 'manufacturer']


class ProcurementAdmin(admin.ModelAdmin):
    list_display = ['process', 'procurement_type', 'owner', 'equipment',
                    'supplier', 'availability', 'min_order_quantity',
                    'price_per_unit', 'currency', 'payment_terms',
                    'delivery_time', 'ce_certified', 'fda_certified']
    list_filter = ['procurement_type', 'owner', 'equipment', 'supplier']


class SupplierAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'lead', 'origin']
    list_filter = [('origin', CountryFilter)]


class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ['process', 'code', 'creation_date', 'payment_method',
                    'payment_date']
    list_filter = ['payment_method']


class StockAdmin(admin.ModelAdmin):
    list_display = ['process', 'owner', 'loading_point', 'creation_date',
                    'quantity', 'warehouse']


class DistributionAdmin(admin.ModelAdmin):
    list_display = ['process', 'distributor', 'location']
    list_filter = ['location']


admin.site.register(Process, ProcessAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(HealthUnit)
admin.site.register(HealthProfessional)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Manufacturer)
admin.site.register(Procurement, ProcurementAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(ProcurementDocument)
admin.site.register(DocumentType)
admin.site.register(PurchaseOrder, PurchaseOrderAdmin)
admin.site.register(Stock, StockAdmin)
admin.site.register(Warehouse)
admin.site.register(Distribution, DistributionAdmin)
admin.site.register(Distributor)