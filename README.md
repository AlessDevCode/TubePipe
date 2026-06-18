# 🚀 TubePipe

¡Bienvenido a **TubePipe**! Esta es una aplicación web diseñada para descargar videos (**MP4**) y audios (**MP3** y **M$A**) de manera rápida y sencilla.

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
```

Cuando termine, puedes cerrar la terminal.

### Si usas Linux (Ubuntu/Debian)

Abre tu terminal y ejecuta:

```bash
sudo apt update && sudo apt install ffmpeg -y
```

### Si usas macOS (Mac)
Abre tu terminal e instala FFmpeg usando Homebrew:

```bash
brew install ffmpeg
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

### En Windows (Si usas Git Bash):

```bash
source env_tubepipe/Scripts/activate
```
### En Windows (Si usas la terminal común CMD):

```dos
env_tubepipe\Scripts\activate.bat
```

### En Linux/Mac:

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

### ¿Para qué sirve el usuario administrador?
Una vez creado, podrás ingresar a http://127.0.0.1:8000/admin/ desde tu navegador. En este panel de control podrás:

- Gestionar y eliminar usuarios registrados.

- Revisar la tabla Download records, donde verás los títulos, URLs y estados de todas las descargas del sistema. Si necesitas limpiar la base de datos para hacer pruebas desde cero, podrás borrar los registros masivamente desde aquí de forma segura.

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

### ✅ ¡Listo!

La terminal del frontend te mostrará una dirección local, normalmente algo parecido a:

```text
http://localhost:5173/
```

Copia esa dirección, pégala en tu navegador y disfruta de **TubePipe** 🚀

## 🔒 Nota Clave sobre la Seguridad y Uso de TubePipe
Para que la aplicación funcione correctamente, el sistema cuenta con un sistema de usuarios estricto y protegido:

- Es obligatorio registrarse e iniciar sesión: No podrás ingresar a la pantalla de descargas ni enviar links de manera anónima. Si intentas escribir la URL de descarga directamente en el navegador, el backend te rechazará con un error de credenciales.

- Historial Privado: Cada usuario registrado verá únicamente las canciones y videos que él mismo ha descargado. Tus descargas están completamente protegidas de otros usuarios.

- Estructura Organizada en el Servidor: Cuando realices una descarga exitosa, el backend creará automáticamente una carpeta con tu nombre de usuario dentro de la carpeta downloads_media/ en el servidor, manteniendo todos tus archivos aislados y ordenados.

## ⚡ Método Avanzado: Ejecutar Backend y Frontend con un solo comando

Si prefieres no tener que abrir dos terminales separadas cada vez que vas a programar, puedes automatizar el arranque de ambos servidores utilizando un único comando en la carpeta del frontend.

### 1. Instalar `concurrently` en el Frontend
Abre tu terminal, entra a la carpeta de React e instala la herramienta de desarrollo:
```bash
cd frontend
npm install concurrently --save-dev
```

### 2. Modificar el package.json del Frontend
Abre el archivo package.json que está dentro de la carpeta frontend. En la sección de "scripts", modifica la línea "dev".

En lugar de usar un comando de Python global (que requeriría activar el entorno virtual manualmente en esa terminal), apuntaremos directamente al ejecutable de Python que vive dentro de nuestra "burbuja" (env_tubepipe):

```json
"scripts": {
  "dev": "concurrently \"cd ../backend && ./env_tubepipe/bin/python manage.py runserver\" \"vite\"",
  "build": "vite build",
  "lint": "eslint .",
  "preview": "vite preview"
}
```
> (Nota: Si no usas Vite y tu script original usaba next o react-scripts start, simplemente reemplaza la palabra "vite" al final por tu comando original).
> (Nota para usuarios de Windows: Si en lugar de usar Git Bash utilizas la terminal nativa CMD de Windows, la ruta del entorno virtual utiliza barras invertidas: .\env_tubepipe\Scripts\python.exe).

#### ¿Cómo se ejecuta ahora?
A partir de este momento, tu flujo de trabajo se reduce a una sola ventana de terminal:

1. Abre la terminal en la raíz del proyecto.

2. Ve a la carpeta de React: cd frontend

3. Ejecuta el comando de desarrollo: npm run dev

#### 💡 ¿Por qué esta configuración es mucho más robusta y cómoda?
Nota importante: Aunque en los pasos anteriores de esta guía se detalla cómo levantar cada servidor de forma manual (lo cual requiere usar comandos como source activate para encender el entorno virtual), con esta nueva configuración ya no necesitas activar el entorno virtual por tu cuenta.

La combinación de la librería concurrently y la ruta directa al entorno virtual funciona como un director de orquesta inteligente:

- Ruta directa al motor: Al escribir ./env_tubepipe/bin/python, le indicas al sistema la ubicación exacta del Python que tiene instaladas las librerías del proyecto (yt-dlp, django, etc.), evitando errores si tienes otras versiones de Python en tu computadora.

- Automatización: El comando retrocede un nivel en tus carpetas (cd ../backend), busca el entorno virtual y arranca el servidor de Django en segundo plano de manera automática.

- Simultaneidad: Al mismo tiempo, enciende el servidor local de React (Vite).

- Consolidación: Junta las respuestas, procesos y errores de ambos servidores en la misma pantalla para que monitorees todo en un solo lugar. Al presionar Ctrl + C, cerrará ambos procesos en simultáneo de forma segura.

> (Nota para usuarios de Windows usando Concurrently: Si al ejecutar npm run dev ves un error que dice que "python3" no se reconoce como un comando, abre el package.json de tu frontend y cambia la palabra python3 por python en la línea de los scripts.)

## README.md y .gitignore

### ¿Qué es y para qué sirve el archivo .gitignore? (Explicación simple)
Imagínalo como una "capa de invisibilidad" o una lista negra para Git.

Cuando trabajamos en un proyecto de programación, la computadora genera cientos de archivos automáticos que nosotros no escribimos (como las librerías de Node.js o Python, archivos temporales del sistema, o bases de datos locales con nuestras contraseñas de prueba). Si subiéramos todo eso a GitHub, el repositorio se volvería extremadamente pesado, lento y, peor aún, inseguro.

El archivo .gitignore le dice a Git: "Oye, mantén un ojo en mi código, pero ignora por completo y no subas a internet ninguna de las carpetas o archivos que están anotados en esta lista".

En TubePipe, nuestro .gitignore está configurado específicamente para proteger tres cosas:

1. Tu privacidad: Evita que se suba la base de datos local (db.sqlite3) con tus usuarios de prueba o contraseñas.

2. El rendimiento de GitHub: Ignora carpetas gigantescas como node_modules o el entorno virtual (env_tubepipe), ya que estas se pueden volver a generar en cualquier computadora con un solo comando.

3. El almacenamiento: Bloquea la carpeta downloads_media, asegurando que los videos o canciones pesadas que descargues para probar la app se queden guardados únicamente en tu computadora y no llenen tu cuenta de GitHub.

### ¿Qué es y para qué sirve el archivo README.md? (Explicación simple)

El archivo README.md (que se traduce literalmente como "LÉEME") es la carta de presentación, el manual de instrucciones y la portada de cualquier proyecto de software. La extensión .md significa Markdown, que es un formato de texto simple que permite añadir negritas, títulos y listas de forma elegante.

Cuando entras a un repositorio en GitHub, lo primero que ves abajo es justamente el contenido de este archivo.

Su objetivo principal es responderle a cualquier programador o usuario que acabe de llegar las siguientes preguntas:

1. ¿Qué hace este proyecto? (En nuestro caso, una aplicación para descargar videos y audios).

2. ¿Qué tecnologías utiliza? (Django, React, yt-dlp, FFmpeg).

3. ¿Cómo lo hago funcionar en mi computadora? (Toda la guía paso a paso de comandos e instalaciones que estás leyendo ahora mismo).

En pocas palabras: sin un README.md, el proyecto sería una caja negra llena de carpetas confusas. Gracias a él, cualquiera puede entender el propósito de TubePipe e instalarlo en minutos sin perderse en el intento.

## Extra
### ¿Qué es y para que sirve el script ver_arbol.py? (Esta en la raiz)
Cuando un proyecto de programación crece, se llena de miles de archivos automáticos pesados (como las librerías de node_modules o los archivos internos de Python). Si intentáramos ver todas las carpetas con un comando común del sistema, la pantalla se inundaría de texto basura y sería imposible entender cómo está organizado nuestro código.

`ver_arbol.py` es un mapeador inteligente de directorios hecho en Python. Su única función es leer la carpeta actual y dibujar en la terminal un esquema visual (un "árbol") limpio y estético de nuestro proyecto, mostrando únicamente los archivos de código reales que nosotros escribimos y modificamos.

### 🔍 ¿Cómo funciona por dentro?
El script es muy elegante y sigue tres pasos clave:

1. El Filtro de Invisibilidad (Líneas 4 a 9): El script tiene dos listas estrictas:

   - extensiones_validas / archivos_validos: Le dicen qué archivos sí nos interesan ver (como .jsx, .py, .json, .gitignore, etc.).

   - carpetas_ignoradas: Esta es la parte más importante. Le prohíbe explícitamente al script entrar a carpetas gigantescas como node_modules, env_tubepipe o .git. Así se evita que la terminal colapse mostrando código ajeno.

2. El Organizador Visual (Línea 32): Para que el árbol se vea hermoso y profesional, el script ordena todo alfabéticamente, pero con una regla de oro: las carpetas siempre van arriba y los archivos sueltos van abajo.

3. El Efecto Cascada o Recursividad (Línea 42): Aquí ocurre la magia. El script utiliza una técnica llamada recursividad (la función mostrar_arbol se llama a sí misma). Si encuentra una carpeta permitida (como backend), entra en ella, dibuja lo que hay dentro usando símbolos como ├── o └──, y si encuentra otra subcarpeta dentro, vuelve a entrar hasta terminar con todo el proyecto.

### 🚀 ¿Cómo se utiliza?
Para ver la estructura limpia de TubePipe en cualquier momento, solo debes abrir tu terminal en la raíz del proyecto y ejecutar:

```bash
python ver_arbol.py
```
(Recuerda que en Linux o Mac, puede que necesites escribir python3 ver_arbol.py).

El resultado será un mapa perfecto en texto plano que puedes copiar y pegar directamente en tus notas o documentación para presumir el orden de tu arquitectura. ¡Es un excelente añadido para el flujo de desarrollo!

## ☕ Apoya el proyecto

**TubePipe** es un proyecto de código abierto desarrollado con mucho entusiasmo para facilitar la descarga de contenido multimedia. Lograr la arquitectura multiusuario, asegurar los endpoints con JWT y sincronizar todo con entornos virtuales tomó bastantes horas de pruebas y café.

Si esta herramienta te resulta útil, te ahorra tiempo o te sirve para tus propios desarrollos, ¡puedes apoyarme! 

🚀 [Invítame un café en Ko-fi](https://ko-fi.com/alesdevcode)

¡Cualquier apoyo o una simple en el repositorio se agradece de corazón!
