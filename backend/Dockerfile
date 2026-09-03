FROM python:3.11-slim

# Instalar FFmpeg y librerías del sistema
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Recopilar archivos estáticos de Django
RUN python manage.py collectstatic --noinput

# Puerto que usará Render
EXPOSE 10000

# Comando para iniciar el backend con Gunicorn
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:10000"]