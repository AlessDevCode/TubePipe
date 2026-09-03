import os
import re
import json
import logging
import tempfile
import urllib.request
import requests
import yt_dlp
from yt_dlp.utils import DownloadError
from django.conf import settings
from django.http import FileResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import DownloadRecord
from .serializers import DownloadRecordSerializer

logger = logging.getLogger(__name__)


def unshorten_url(url):
    """Resuelve enlaces acortados (ej: vt.tiktok.com)."""
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.geturl()
    except Exception:
        return url


def extract_tiktok_photo_audio(url, output_path):
    """Extrae directamente la pista de audio de un carrusel /photo/ de TikTok mediante análisis multinivel."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        html = response.text
    except Exception as e:
        return False, f"Error al conectar con TikTok: {str(e)}", None

    play_url = None
    title = "TikTok Audio"

    # 1. Búsqueda directa por patrones de URL de audio en CDN de TikTok (.mp3 o parámetros de audio)
    audio_matches = re.findall(
        r'https://[^\s"\'<>]+(?:tik-tok|tiktokcdn|akamaized)[^\s"\'<>]+(?:\.mp3|\?mime_type=audio_mp3|/play/)[^\s"\'<>]*', 
        html
    )
    if audio_matches:
        play_url = audio_matches[0]

    # 2. Búsqueda secundaria de llaves playUrl o play_url en el texto plano
    if not play_url:
        raw_urls = re.findall(r'"playUrl"\s*:\s*"([^"]+)"', html) or re.findall(r'"play_url"\s*:\s*"([^"]+)"', html)
        if raw_urls:
            play_url = raw_urls[0]

    # 3. Búsqueda recursiva profunda dentro de bloques JSON rehidratados (SIGI_STATE, __UNIVERSAL_DATA..., etc)
    if not play_url:
        for script_id in ['__UNIVERSAL_DATA_FOR_REHYDRATION__', 'SIGI_STATE', '__NEXT_DATA__']:
            match = re.search(f'<script id="{script_id}"[^>]*>(.*?)</script>', html)
            if match:
                try:
                    data = json.loads(match.group(1))

                    def search_audio_key(item):
                        if isinstance(item, dict):
                            for k, v in item.items():
                                if k in ['playUrl', 'play_url'] and isinstance(v, str) and v.startswith('http'):
                                    return v
                                res = search_audio_key(v)
                                if res: 
                                    return res
                        elif isinstance(item, list):
                            for element in item:
                                res = search_audio_key(element)
                                if res: 
                                    return res
                        return None

                    play_url = search_audio_key(data)
                    if play_url:
                        break
                except Exception:
                    pass

    if not play_url:
        return False, "No se pudo extraer el enlace de la pista de audio en esta publicación.", None

    # Limpiar formato de URL codificada
    play_url = play_url.replace(r'\u002F', '/').replace(r'\/', '/').replace(r'\u0026', '&')

    # Descargar el archivo binario del audio
    try:
        audio_req = requests.get(play_url, headers=headers, timeout=15)
        if audio_req.status_code == 200 and len(audio_req.content) > 1000:
            with open(output_path, 'wb') as f:
                f.write(audio_req.content)
            return True, output_path, title
        else:
            return False, "La respuesta del servidor de audio de TikTok no fue válida.", None
    except Exception as e:
        return False, f"Error de descarga binaria: {str(e)}", None


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_history(request):
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

    processed_url = unshorten_url(url)
    record = DownloadRecord.objects.create(url=url, status='pending', user=request.user)

    user_folder = os.path.join(settings.MEDIA_ROOT, request.user.username)
    os.makedirs(user_folder, exist_ok=True)

    # MANEJO AUTOMÁTICO PARA PUBLICACIONES DE FOTOS (/photo/)
    if '/photo/' in processed_url:
        if file_format == 'mp4':
            file_format = 'mp3'
        
        target_filename = os.path.join(user_folder, f"audio_tiktok_{record.id}.{file_format}")
        success, result_path, title = extract_tiktok_photo_audio(processed_url, target_filename)

        if success and os.path.exists(result_path):
            record.title = title[:100] if title else "TikTok Audio"
            record.duration = 0
            record.status = 'completed'
            record.save()
            return FileResponse(open(result_path, 'rb'), as_attachment=True)
        else:
            record.status = 'failed'
            record.save()
            return Response({"error": result_path if isinstance(result_path, str) else "Error al extraer el audio del carrusel."}, status=status.HTTP_400_BAD_REQUEST)

    # FLUJO ESTÁNDAR CON YT-DLP (Para videos normales)
    cookie_file = None
    try: 
        out_template = os.path.join(user_folder, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': out_template,
            'noplaylist': True,
            'ffmpeg_location': '/usr/bin/ffmpeg',
            # Simular clientes móviles para evitar la detección de IP de Render/datacenter
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios', 'android', 'mweb'],
                }
            },
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            }
        }

        # Manejo seguro de cookies en directorio temporal (/tmp) con formato estricto
        cookies_content = os.environ.get('YOUTUBE_COOKIES')
        if cookies_content:
            cookies_content = cookies_content.strip()
            # Garantizar que contenga el encabezado requerido por yt-dlp
            if not cookies_content.startswith('# Netscape'):
                cookies_content = "# Netscape HTTP Cookie File\n" + cookies_content

            cookie_file = tempfile.NamedTemporaryFile(mode='w', delete=False, dir='/tmp', suffix='.txt')
            cookie_file.write(cookies_content)
            cookie_file.flush()
            cookie_file.close()
            ydl_opts['cookiefile'] = cookie_file.name

        if file_format == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            })
        elif file_format == 'm4a':
            ydl_opts.update({
                'format': 'bestaudio[ext=m4a]/bestaudio',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'm4a',
                }],
            })
        else:
            ydl_opts.update({
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(processed_url, download=True)
            filename = ydl.prepare_filename(info)
            
            if file_format == 'mp3':
                filename = os.path.splitext(filename)[0] + '.mp3'
            elif file_format == 'm4a':
                filename = os.path.splitext(filename)[0] + '.m4a'
            
            record.title = info.get('title', 'Video sin título')
            record.duration = info.get('duration', 0)
            record.status = 'completed'
            record.save()

        if os.path.exists(filename):
            return FileResponse(open(filename, 'rb'), as_attachment=True)
        else:
            raise FileNotFoundError("El archivo procesado no se encontró.")

    except DownloadError as e:
        logger.error(f"Error de yt-dlp: {str(e)}")
        record.status = 'failed'
        record.save()
        return Response({"error": "YouTube bloqueó la descarga o requiere verificación de bot."}, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        logger.error(f"Error interno: {str(e)}")
        record.status = 'failed'
        record.save()
        return Response({"error": "Error interno del servidor al procesar el archivo."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    finally:
        # Garantiza la destrucción inmediata del archivo de cookies
        if cookie_file and os.path.exists(cookie_file.name):
            try:
                os.remove(cookie_file.name)
            except Exception:
                pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_history(request, pk):
    try:
        record = DownloadRecord.objects.get(pk=pk, user=request.user)
        record.delete()
        return Response({"message": "Registro eliminado correctamente del historial."}, status=status.HTTP_200_OK)
    except DownloadRecord.DoesNotExist:
        return Response({"error": "El registro no existe o no tienes permisos para eliminarlo."}, status=status.HTTP_404_NOT_FOUND)