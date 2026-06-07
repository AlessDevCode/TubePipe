# 🚀 TubePipe

¡Bienvenido a **TubePipe**! Esta es una aplicación web diseñada para descargar videos (**MP4**) y audios (**MP3**) de manera rápida y sencilla.

Este proyecto está dividido en dos partes:

- **Backend (El motor oculto):** Construido con **Python y Django**.
- **Frontend (La cara visual):** Construido con **React y Node.js**.

Si es tu primera vez programando o clonando un proyecto, no te preocupes. Esta guía te llevará paso a paso para que tu computadora tenga todo lo necesario para ejecutar **TubePipe** sin errores.

---

# 🛠️ Paso 1: Preparar tu computadora (Requisitos Previos)

Antes de descargar el código, tu computadora necesita tener instaladas ciertas herramientas.

## 1. Instalar Node.js (Para el Frontend)

Node.js es el entorno que permite ejecutar React.

1. Ve a la página oficial:  
   https://nodejs.org/

2. Descarga la versión que dice **LTS** (Recomendada para la mayoría de los usuarios).

3. Instálalo dando **Siguiente** a todo.

---

## 2. Instalar FFmpeg (Para procesar los videos)

`FFmpeg` es un programa invisible pero crucial. Es el motor que usa nuestra librería para unir el video con el audio y convertirlos a **MP4** o **MP3**.

### Si usas Windows

Abre tu terminal (**Windows + R → cmd → Enter**) y ejecuta:

```cmd
winget install Gyan.FFmpeg

Cuando termine, puedes cerrar la terminal.

### Si usas Linux (Ubuntu/Debian)

Abre tu terminal y ejecuta:

```bash
sudo apt update && sudo apt install ffmpeg -y
```

---

## 3. Instalar Git y Git Bash (Para descargar el código)

Git es la herramienta que usan los programadores para compartir código.

### Si usas Linux

Generalmente ya viene instalado. Si no, ejecuta:

```bash
sudo apt install git
```

### Si usas Windows

1. Ve a:
   https://git-scm.com/download/win

2. Descarga el instalador de **64-bit**.

3. Ejecuta el instalador.

4. Verás muchas pantallas con opciones complejas. **No te preocupes**: simplemente dale a **Next (Siguiente)** a todo dejando la configuración por defecto.

Esto instalará **Git Bash**, una terminal especial que utilizaremos de ahora en adelante.

---

# 🐙 Paso 2: Crear tu cuenta de GitHub y clonar el proyecto

## 1. Crear una cuenta de GitHub

Ve a:

https://github.com/

Haz clic en **Sign up** y crea una cuenta gratuita si aún no la tienes.

---

## 2. Clonar (Descargar) el proyecto

1. Crea una carpeta vacía donde quieras guardar el proyecto.

2. Haz clic derecho dentro de esa carpeta y selecciona:

```text
Open Git Bash here
```

> En Windows 11 puede que primero debas pulsar **“Mostrar más opciones”**.

3. En la terminal negra que se abre, ejecuta:

```bash
git clone ENLACE_DEL_REPOSITORIO.git
```

> Debes pedir el enlace real del repositorio al creador del proyecto.

### Inicio de sesión en GitHub

Al ejecutar el comando, GitHub puede pedirte iniciar sesión para verificar tu cuenta.

Normalmente aparecerá una ventana emergente o el navegador solicitando autorización para **Git Credential Manager**.

Simplemente:

1. Haz clic en **Sign in with browser**.
2. Inicia sesión con tu cuenta de GitHub.
3. Autoriza el acceso.

Después de eso, el proyecto empezará a descargarse.

---

# ⚙️ Paso 3: Configurar el Backend (Django)

Ahora vamos a instalar las dependencias del motor de **Python**.

Todo esto se hace desde **Git Bash**.

## 1. Entrar al proyecto

Entra a la carpeta del proyecto y luego al backend:

```bash
cd NombreDeLaCarpetaDelProyecto
cd backend
```

---

## 2. Crear un entorno virtual

Un entorno virtual es una “burbuja” aislada para que las librerías del proyecto no afecten tu computadora.

Ejecuta:

```bash
python -m venv env_tubepipe
```

> En Linux o Mac, puede que necesites usar `python3` en lugar de `python`.

---

## 3. Activar el entorno virtual

### En Windows

```bash
source env_tubepipe/Scripts/activate
```

### En Linux/Mac

```bash
source env_tubepipe/bin/activate
```

Sabrás que funcionó porque aparecerá algo así al inicio de la terminal:

```text
(env_tubepipe)
```

---

## 4. Instalar las dependencias del backend

Ejecuta:

```bash
pip install -r requirements.txt
```

---

## 5. Crear la base de datos local

Ejecuta:

```bash
python manage.py migrate
```

---

## 6. Crear un usuario administrador(opcional)

Ejecuta:

```bash
python manage.py createsuperuser
```

Te pedirá:

* Nombre de usuario
* Correo electrónico
* Contraseña

> La contraseña no se verá mientras escribes. Es completamente normal.

---

# 🎨 Paso 4: Configurar el Frontend (React)

El frontend necesita descargar sus propios paquetes de **Node.js**.

Abre una nueva terminal en la raíz del proyecto y entra a la carpeta frontend.

```bash
cd frontend
```

Instala todos los módulos necesarios:

```bash
npm install
```

---

# 🟢 Paso 5: ¡Arrancar el proyecto!

Cada vez que quieras programar o usar **TubePipe**, debes iniciar ambos servidores.

## 1. Encender el Backend

En la primera terminal, asegúrate de estar en:

```text
backend/
```

Con el entorno virtual activado, ejecuta:

```bash
python manage.py runserver
```

---

## 2. Encender el Frontend

En una segunda terminal, asegúrate de estar en:

```text
frontend/
```

Y ejecuta:

```bash
npm run dev
```

---

# ✅ ¡Listo!

La terminal del frontend te mostrará una dirección local, normalmente algo parecido a:

```text
http://localhost:5173/
```

Copia esa dirección, pégala en tu navegador y disfruta de **TubePipe** 🚀

```
```
