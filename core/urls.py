from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Rasmlar uchun kerakli Django sozlamalari import qilindi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Water Distribution API",
        default_version='v1',
        description="Suv tarqatish biznesi – mahsulotlar, mijozlar va fakturalar boshqaruvi",
        contact=openapi.Contact(email="admin@water.uz"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Root redirect to dashboard
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),

    path('admin/', admin.site.urls),

    # API endpoints
    path('api/', include('water.urls')),

    # JWT auth
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Swagger docs
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # Frontend views
    path('dashboard/', include('water.frontend_urls')),
]

# Agar DEBUG faol bo'lsa, yuklangan rasmlarni brauzerda ochishga ruxsat berish
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)