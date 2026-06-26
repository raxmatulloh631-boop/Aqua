from django.urls import path
from . import frontend_views as v

urlpatterns = [
    path('', v.dashboard, name='dashboard'),
    path('login/', v.login_view, name='login'),
    path('logout/', v.logout_view, name='logout'),

    # Products
    path('products/', v.product_list, name='product_list'),
    path('products/new/', v.product_create, name='product_create'),
    path('products/<int:pk>/edit/', v.product_edit, name='product_edit'),
    path('products/<int:pk>/delete/', v.product_delete, name='product_delete'),

    # Customers
    path('customers/', v.customer_list, name='customer_list'),
    path('customers/new/', v.customer_create, name='customer_create'),
    path('customers/<int:pk>/edit/', v.customer_edit, name='customer_edit'),
    path('customers/<int:pk>/delete/', v.customer_delete, name='customer_delete'),

    # Invoices
    path('invoices/', v.invoice_list, name='invoice_list'),
    path('invoices/new/', v.invoice_create, name='invoice_create'),
    path('invoices/<int:pk>/delete/', v.invoice_delete, name='invoice_delete'),
]
