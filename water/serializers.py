from rest_framework import serializers
from .models import Product, Customer, Invoice, InvoiceItem


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class InvoiceItemSerializer(serializers.ModelSerializer):
    product_name = serializers.ReadOnlyField(source='product.name')
    product_price = serializers.ReadOnlyField(source='product.price')

    class Meta:
        model = InvoiceItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'item_total_price']
        read_only_fields = ['item_total_price']


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)
    customer_name = serializers.ReadOnlyField(source='customer.name')

    class Meta:
        model = Invoice
        fields = ['id', 'customer', 'customer_name', 'items', 'total_price', 'created_at']
        read_only_fields = ['total_price', 'created_at']

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, **item_data)

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop('items', None)
        instance.customer = validated_data.get('customer', instance.customer)
        instance.save()

        if items_data is not None:
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(invoice=instance, **item_data)

        return instance