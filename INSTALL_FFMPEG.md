# 🛠️ Guía de Instalación de FFmpeg

**Idioma:** 🇪🇸 Español | 🇬🇧 [English](INSTALL_FFMPEG.en.md)

Los scripts de este toolkit dependen de **FFmpeg**, una herramienta gratuita de código abierto para procesar audio y video.

Si al ejecutar los scripts te aparece el error: `FileNotFoundError: [WinError 2]`, significa que FFmpeg no está instalado o no está en el PATH de tu sistema. Sigue estos pasos según tu sistema operativo:

---

## 🪟 Para usuarios de Windows

### Paso 1: Descargar

1. Ve a la página oficial: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Pasa el cursor sobre el logo de Windows y haz clic en uno de los enlaces de compilación (ej. _gyan.dev_ o _BtbN_).
3. Descarga el archivo `.zip` de la versión "Release" o "Master".

### Paso 2: Extraer

1. Crea una carpeta en tu disco local C: llamada `FFmpeg` (Ruta: `C:\FFmpeg`).
2. Descomprime el contenido del `.zip` dentro de esa carpeta.
3. Asegúrate de que el archivo `ffmpeg.exe` esté ubicado en `C:\FFmpeg\bin\ffmpeg.exe`.

### Paso 3: Agregar al PATH (¡Importante!)

Para que Python pueda "ver" FFmpeg, debes agregarlo a las variables de entorno de Windows:

1. Presiona la tecla `Windows` y busca **"Variables de entorno"** (o "Environment variables").
2. Haz clic en el botón **"Variables de entorno..."** en la parte inferior derecha.
3. En la sección "Variables del sistema" (abajo), busca la variable llamada `Path`, selecciónala y haz clic en **Editar**.
4. Haz clic en **Nuevo** y pega la ruta a tu carpeta bin: `C:\FFmpeg\bin`
5. Haz clic en **Aceptar** en todas las ventanas.

_(Nota: Deberás cerrar y volver a abrir cualquier terminal de CMD o VS Code que tuvieras abierta para que los cambios surtan efecto)._

---

## 🍏 Para usuarios de macOS (Mac)

La forma más sencilla es usar Homebrew. Abre tu Terminal y ejecuta:

```bash
brew install ffmpeg

🐧 Para usuarios de Linux

Abre tu terminal y ejecuta el comando según tu distribución:

Ubuntu / Debian:
Bash

sudo apt update && sudo apt install ffmpeg

Arch Linux:
Bash

sudo pacman -S ffmpeg

✅ Verificar la instalación

Para comprobar que todo está listo, abre una terminal (CMD, PowerShell o Terminal) y escribe:
Bash

ffmpeg -version

Si ves un texto largo con la versión y detalles de configuración, ¡estás listo para usar el OGG Toolkit!
```
