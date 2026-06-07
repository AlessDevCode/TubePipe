from django.db import models

class DownloadRecord(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('completed', 'Completado'),
        ('failed', 'Fallido'),
    ]

    title = models.CharField(max_length=255, blank=True, null=True)
    url = models.URLField()
    duration = models.IntegerField(blank=True, null=True)  # Guardaremos la duración en segundos
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)   # Fecha y hora automática de registro

    def __str__(self):
        return self.title if self.title else self.url