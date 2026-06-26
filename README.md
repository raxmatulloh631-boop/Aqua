# 💧 AquaBiz – Suv Tarqatish Boshqaruv Tizimi

Django REST Framework + Templates bilan qurilgan production-ready MVP.

## 🚀 Tez Ishga Tushirish

```bash
# 1. Virtual muhit yarating
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows

# 2. Kutubxonalarni o'rnating
pip install -r requirements.txt

# 3. Ma'lumotlar bazasini yarating
python manage.py migrate

# 4. Admin va namuna ma'lumotlar yaratish
python setup.py

# 5. Serverni ishga tushiring
python manage.py runserver
```

**Kirish:** http://127.0.0.1:8000  
**Login:** `admin` | **Parol:** `admin123`

## 📦 URL Manzillar

| Sahifa | URL |
|--------|-----|
| Dashboard | http://127.0.0.1:8000/dashboard/ |
| Admin | http://127.0.0.1:8000/admin/ |
| API Docs (Swagger) | http://127.0.0.1:8000/api/docs/ |
| API Products | http://127.0.0.1:8000/api/products/ |
| API Customers | http://127.0.0.1:8000/api/customers/ |
| API Invoices | http://127.0.0.1:8000/api/invoices/ |
| JWT Token | http://127.0.0.1:8000/api/token/ |

## 🐳 Docker bilan

```bash
docker-compose up --build
python manage.py migrate
python setup.py
```

## ✅ Tuzatilgan Xatolar

1. `serializer_name` → `serializer_class` (ViewSet'larda)
2. `drf_yasg` to'g'ri o'rnatildi va settings'ga qo'shildi
3. `drf_spectacular` + `drf_yasg` konflikti hal qilindi
4. `STATICFILES_DIRS` to'g'ri sozlandi
5. Templates to'liq yaratildi
