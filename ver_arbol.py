import os

def mostrar_arbol(ruta=".", prefijo=""):
    # 1. Extensiones permitidas (Se agregó '.py')
    extensiones_validas = {'.jsx', '.js', '.ts', '.tsx', '.css', '.html', '.json', '.md', '.py'}
    archivos_validos = {'.gitignore', 'package.json', 'package-lock.json'}
    
    # 2. Carpetas del sistema y de dependencias (node_modules incluido)
    carpetas_ignoradas = {'.git', '.venv', '__pycache__', '.vscode', 'env', 'venv', 'env_tubepipe', 'node_modules', 'dist', 'build'}

    try:
        items = os.listdir(ruta)
    except PermissionError:
        return

    # Filtrar elementos
    items_filtrados = []
    for item in items:
        if item in carpetas_ignoradas:
            continue
            
        full_path = os.path.join(ruta, item)
        
        if os.path.isdir(full_path):
            items_filtrados.append(item)
        else:
            _, ext = os.path.splitext(item)
            if ext in extensiones_validas or item in archivos_validos:
                items_filtrados.append(item)

    # Ordenar: Carpetas primero, luego archivos
    items_filtrados.sort(key=lambda x: (not os.path.isdir(os.path.join(ruta, x)), x.lower()))

    # Dibujar la estructura
    for i, item in enumerate(items_filtrados):
        es_ultimo = (i == len(items_filtrados) - 1)
        simbolo = "└── " if es_ultimo else "├── "
        
        print(f"{prefijo}{simbolo}{item}")
        
        full_path = os.path.join(ruta, item)
        if os.path.isdir(full_path):
            nuevo_prefijo = prefijo + ("    " if es_ultimo else "│   ")
            mostrar_arbol(full_path, nuevo_prefijo)

if __name__ == "__main__":
    print("Estructura del Proyecto:")
    print(".")
    mostrar_arbol()