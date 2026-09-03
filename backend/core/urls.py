from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Rutas para autenticación
    path('api/auth/', include('apps.users.urls')), # Incluye tu register/ de apps.users
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Rutas de descargas (si tienes la app downloads)
    path('api/downloads/', include('apps.downloads.urls')),
]