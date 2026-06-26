from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CustomerViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'customers', CustomerViewSet, basename='customer')
router.register(r'invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]
