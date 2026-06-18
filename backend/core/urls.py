from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Endpoints de Autenticación y Gestión de Usuarios
    path('api/auth/', include('apps.users.urls')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # Servirá como LOGIN
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Endpoints del Historial de Descargas
    path('api/', include('apps.downloads.urls')),
]