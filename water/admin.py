from django.contrib import admin
from .models import Product, Customer, Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1
    readonly_fields = ['item_total_price']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock']
    list_filter = ['stock']
    search_fields = ['name']


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'address']
    search_fields = ['name', 'phone']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['pk', 'customer', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__name']
    readonly_fields = ['total_price', 'created_at']
    inlines = [InvoiceItemInline]