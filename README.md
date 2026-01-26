# 🎵 OGG Audio Optimization Toolkit

> **Un conjunto de herramientas de automatización en Python para convertir, comprimir y organizar archivos de audio, optimizados especialmente para el formato Vorbis (OGG) en desarrollo web y de videojuegos.**

Este toolkit está diseñado para creadores de contenido, desarrolladores indie y diseñadores web que necesitan procesar lotes masivos de audio, reducir el peso de los archivos sin perder calidad aparente, y organizar sus carpetas de recursos (assets) con un solo comando.

## ✨ El Ecosistema (Scripts Disponibles)

El toolkit se compone de 4 scripts independientes que cubren todo el flujo de trabajo de audio:

### 1. 🔄 `converter-ogg.py` (Conversor Universal)

- **Función:** Busca recursivamente en una carpeta archivos `.mp3`, `.wav`, `.flac`, `.aac` o `.m4a` y los convierte al formato `.ogg` (libvorbis).
- **Uso ideal:** Estandarizar todos los efectos de sonido o música de un proyecto a un formato ligero y sin licencias (open-source).

### 2. 🗂️ `separate-ogg-files.py` (Organizador Automático)

- **Función:** Escanea una carpeta caótica y mueve los archivos a subcarpetas según su extensión (crea carpetas `/mp3`, `/ogg`, `/wav`, etc.).
- **Uso ideal:** Limpiar carpetas de descargas o clasificar assets de audio mezclados.

### 3. 📉 `ogg-compressor.py` (Compresor Relativo - 50%)

- **Función:** Analiza el bitrate original de un archivo `.ogg` y lo recomprime exactamente a la mitad de su peso (mínimo de 32kbps), replicando la estructura de carpetas original en un nuevo destino.
- **Uso ideal:** Reducir a la mitad el peso de una librería de música ya existente sin destrozar la calidad.

### 4. 📦 `ogg-compressor-max.py` (Compresor Absoluto < 1MB)

- **Función:** Calculador inteligente que analiza la duración de la pista y ajusta el bitrate dinámicamente para garantizar que el archivo final **pese menos de 1 MB**.
- **Uso ideal:** Optimizar audios largos (ambientes, música de fondo) para sitios web donde la velocidad de carga (Core Web Vitals) es crítica.

---

## ⚙️ Requisitos e Instalación

**Requisitos del sistema:**

- Python 3.8 o superior.
- **FFmpeg instalado y agregado al PATH del sistema** (Obligatorio, ya que es el motor de conversión subyacente).

### 1. Clonar el repositorio

```bash
git clone [https://github.com/tu-usuario/ogg-audio-toolkit.git](https://github.com/tu-usuario/ogg-audio-toolkit.git)
cd ogg-audio-toolkit
```

2. Instalar dependencias de Python

Solo el script de compresión máxima (ogg-compressor-max.py) requiere una librería externa de Python.
Bash

pip install pydub

📖 Guía de Uso

Los scripts están diseñados para ser interactivos por terminal. Simplemente ejecútalos y te pedirán las rutas de las carpetas.

Ejemplo de flujo de trabajo:

Tienes una carpeta llena de .wav y .mp3. Ejecutas el conversor:
Bash
python converter-ogg.py

# (Ingresas la ruta de tu carpeta)

Ahora separas los originales de los nuevos OGG:
Bash

python separate-ogg-files.py

# (Los OGG se moverán solos a una carpeta /ogg)

Comprimes los OGG para web (forzando a que pesen menos de 1MB):
Bash

python ogg-compressor-max.py

# (Ingresas la ruta de entrada /ogg y una nueva de salida)

⚠️ Notas Técnicas y Limitaciones

FFmpeg PATH: Si obtienes el error FileNotFoundError: [WinError 2] El sistema no puede encontrar el archivo especificado, significa que Python no encuentra ffmpeg. Asegúrate de descargarlo e incluirlo en las Variables de Entorno de Windows/Linux.

Límite de Bitrate (ogg-compressor-max.py): Si intentas comprimir un audio de 10 minutos para que pese 1 MB, el script bajará el bitrate al límite del codec Vorbis (48 kbps). El audio se escuchará "robotizado". Úsalo con criterio según la duración del audio.

No-Destructivo: Ninguno de los scripts borra los archivos originales (excepto el organizador que los mueve de carpeta). Las conversiones generan nuevos archivos.
⚖️ Licencia y Créditos

Este proyecto utiliza librerías de código abierto como pydub y el potente motor de procesamiento multimedia FFmpeg.

Ideal para optimización de assets en Minecraft Texturepacks, Godot, Unity, Unreal Engine y Desarrollo Web.
