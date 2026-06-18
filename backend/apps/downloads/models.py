from django.db import models
from django.contrib.auth.models import User 

class DownloadRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    # Relación multiusuario: Vincula cada descarga a un usuario de Django
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='downloads', null=True, blank=True)
    url = models.URLField()
    title = models.CharField(max_length=255, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        username = self.user.username if self.user else "Anónimo"
        return f"{self.title or self.url} - Descargado por: {username}"