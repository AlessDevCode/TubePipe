from rest_framework import serializers
from .models import DownloadRecord

class DownloadRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = DownloadRecord
        fields = '__all__'  # Esto incluirá todos los campos, incluido el 'user_id' si se requiere en el JSON