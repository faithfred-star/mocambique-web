from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'phone', 'payment_method', 'total_amount', 'created_at', 'is_paid')
    list_filter = ('payment_method', 'delivery_method', 'is_paid', 'created_at')
    search_fields = ('full_name', 'email', 'phone', 'national_id')
    readonly_fields = ('created_at',)
