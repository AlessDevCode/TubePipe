import os
import yt_dlp
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import DownloadRecord
from .serializers import DownloadRecordSerializer

@api_view(['GET'])
def get_history(request):
    """Devuelve la lista de videos descargados ordenados por los más recientes."""
    records = DownloadRecord.objects.all().order_by('-created_at')
    serializer = DownloadRecordSerializer(records, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def download_video(request):
    """
    Recibe la URL y el formato ('mp3' o 'mp4').
    Procesa la descarga dinámicamente y transmite el archivo resultante.
    """
    url = request.data.get('url')
    # Capturamos el formato elegido. Si no se envía ninguno, por defecto será 'mp4'.
    file_format = request.data.get('format', 'mp4')
    
    if not url:
        return Response({"error": "La URL es obligatoria"}, status=status.HTTP_400_BAD_REQUEST)

    if file_format not in ['mp3', 'mp4']:
        return Response({"error": "Formato no válido. Use 'mp3' o 'mp4'."}, status=status.HTTP_400_BAD_REQUEST)

    # Creamos el registro inicial en la base de datos
    record = DownloadRecord.objects.create(url=url, status='pending')

    try:
        # Configuración dinámica de yt-dlp según la solicitud
        if file_format == 'mp3':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads_media/%(title)s.%(ext)s',
                'noplaylist': True,
                # Postprocesador de FFmpeg para extraer el audio y convertirlo limpiamente a MP3
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',  # Excelente relación calidad/peso
                }],
            }
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': 'downloads_media/%(title)s.%(ext)s',
                'noplaylist': True,
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extraemos metadatos y ejecutamos la descarga/conversión
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # NOTA CLAVE: Cuando FFmpeg convierte el archivo a MP3, muta la extensión en el disco.
            # Debemos actualizar la ruta de lectura reemplazando la extensión original por .mp3
            if file_format == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            
            # Actualizamos el registro de la base de datos con los metadatos reales obtenidos
            record.title = info.get('title', 'Audio sin título' if file_format == 'mp3' else 'Video sin título')
            record.duration = info.get('duration', 0)
            record.status = 'completed'
            record.save()

        # Retornamos el archivo binario procesado (sea .mp4 o .mp3)
        if os.path.exists(filename):
            response = FileResponse(open(filename, 'rb'), as_attachment=True)
            return response
        else:
            raise FileNotFoundError("El archivo procesado no se encontró en el servidor.")

    except Exception as e:
        record.status = 'failed'
        record.save()
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)