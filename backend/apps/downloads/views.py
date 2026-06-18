import os
import yt_dlp
from django.conf import settings                                   # <-- 1. IMPORTAMOS LAS CONFIGURACIONES GLOBALES
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DownloadRecord
from .serializers import DownloadRecordSerializer
@api_view(['GET'])
@permission_classes([IsAuthenticated]) # <-- Protege el historial, requiere JWT
def get_history(request):
    """Devuelve la lista de videos descargados EXCLUSIVAMENTE por el usuario autenticado."""
    # Filtramos por request.user para que no vea descargas ajenas
    records = DownloadRecord.objects.filter(user=request.user).order_by('-created_at')
    serializer = DownloadRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def download_video(request):
    url = request.data.get('url')
    file_format = request.data.get('format', 'mp4')
    
    if not url:
        return Response({"error": "La URL es obligatoria"}, status=status.HTTP_400_BAD_REQUEST)

    if file_format not in ['mp3', 'mp4', 'm4a']:
        return Response({"error": "Formato no válido. Use 'mp3', 'mp4' o 'm4a'."}, status=status.HTTP_400_BAD_REQUEST)

    record = DownloadRecord.objects.create(url=url, status='pending', user=request.user)

    try:
        # 2. RESOLUCIÓN LIMPIA DE RUTAS: 
        # Tomamos settings.MEDIA_ROOT y le concatenamos el nombre del usuario logueado
        user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
        
        # Nos aseguramos de que la ruta exista en el disco duro, si no, se crea automáticamente
        os.makedirs(user_folder, exist_ok=True)

        # Plantilla de salida limpia y absoluta para yt-dlp
        out_template = os.path.join(user_folder, '%(title)s.%(ext)s')

        # Configuración condicional del flujo de yt-dlp usando la plantilla limpia
        if file_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': out_template,  # <-- Usamos la variable limpia
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
        elif file_format == 'm4a':
            ydl_opts = {
                'format': 'bestaudio[ext=m4a]/bestaudio',
                'outtmpl': out_template,  # <-- Usamos la variable limpia
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
            }
        else: # mp4
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': out_template,  # <-- Usamos la variable limpia
                'noplaylist': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            if file_format == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            elif file_format == 'm4a':
                filename = os.path.splitext(filename)[0] + '.m4a'
            
            record.title = info.get('title', f'Audio {file_format.upper()} sin título' if file_format != 'mp4' else 'Video sin título')
            record.duration = info.get('duration', 0)
            record.status = 'completed'
            record.save()

        if os.path.exists(filename):
            response = FileResponse(open(filename, 'rb'), as_attachment=True)
            return response
        else:
            raise FileNotFoundError("El archivo procesado no se encontró en el servidor.")

    except Exception as e:
        record.status = 'failed'
        record.save()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated]) # <-- NUEVO: Endpoint de borrado protegido
def delete_history(request, pk):
    """Elimina un registro del historial si pertenece al usuario autenticado."""
    try:
        # Buscamos el registro asegurándonos de que pertenezca a quien hace la petición
        record = DownloadRecord.objects.get(pk=pk, user=request.user)
        record.delete()
        return Response({"message": "Registro eliminado correctamente del historial."}, status=status.HTTP_200_OK)
    except DownloadRecord.DoesNotExist:
        return Response({"error": "El registro no existe o no tienes permisos para eliminarlo."}, status=status.HTTP_404_NOT_FOUND)