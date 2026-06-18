from django.contrib import admin
from .models import DownloadRecord

@admin.register(DownloadRecord)
class DownloadRecordAdmin(admin.ModelAdmin):
    # Columnas que se mostrarán en la lista del panel administrador
    list_display = ('id', 'user', 'title', 'status', 'created_at')
    
    # Filtros laterales para buscar rápidamente por estado o por usuario
    list_filter = ('status', 'user')
    
    # Barra de búsqueda para buscar videos por título o por URL
    search_fields = ('title', 'url')
    
    # Orden por defecto (los más recientes primero)
    ordering = ('-created_at',)