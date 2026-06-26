#!/usr/bin/env python
"""
Loyihani ishga tushirish uchun setup script.
Superuser va namuna ma'lumotlar yaratadi.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from water.models import Product, Customer, Invoice

User = get_user_model()

# ── Superuser ────────────────────────────────────────────────────────────────
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@water.uz', 'admin123')
    print("✅ Superuser yaratildi: admin / admin123")
else:
    print("ℹ️  Superuser allaqachon mavjud")

# ── Sample products ──────────────────────────────────────────────────────────
products_data = [
    {'name': 'BIOLIFE 19L', 'price': 12000, 'stock': 200},
    {'name': 'Aqua Premium 19L', 'price': 10000, 'stock': 150},
    {'name': 'Crystal 5L', 'price': 4000, 'stock': 300},
    {'name': 'NaturAqua 1.5L', 'price': 2500, 'stock': 500},
]
for pd in products_data:
    p, created = Product.objects.get_or_create(name=pd['name'], defaults=pd)
    if created:
        print(f"✅ Mahsulot: {p.name}")

# ── Sample customers ─────────────────────────────────────────────────────────
customers_data = [
    {'name': 'Hilol Market', 'phone': '+998901234567', 'address': 'Toshkent, Yunusobod'},
    {'name': 'Sardor Xoliqov', 'phone': '+998901112233', 'address': 'Toshkent, Mirzo Ulugbek'},
    {'name': 'Baraka Restoran', 'phone': '+998995556677', 'address': 'Toshkent, Chilonzor'},
]
for cd in customers_data:
    c, created = Customer.objects.get_or_create(name=cd['name'], defaults=cd)
    if created:
        print(f"✅ Mijoz: {c.name}")

print("\n🚀 Setup tugadi! http://127.0.0.1:8000/dashboard/ manziliga kiring")
print("   Login: admin | Parol: admin123")
