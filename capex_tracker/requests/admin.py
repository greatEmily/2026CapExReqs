from django.contrib import admin
from .models import Theatre, Equipment, Request

# Register your models here.
@admin.register(Theatre)
class TheatreAdmin(admin.ModelAdmin):
    list_display = ('number', 'name', 'division', 'rvp', 'region')
    search_fields = ('name', 'region', 'rvp')

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'serial_number', 'price')
    search_fields = ('make', 'model')

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'theatre', 'equipment', 'approval_status', 'request_date')
    list_filter = ('approval_status', 'request_date')
    search_fields = ('requisition_number', 'po_number')
