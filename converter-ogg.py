import os
import subprocess

# Extensiones de audio a convertir
AUDIO_FORMATOS = (".mp3", ".wav", ".flac", ".aac", ".m4a")

def convertir_a_ogg(ruta_archivo):
    nombre_sin_ext, _ = os.path.splitext(ruta_archivo)
    ruta_salida = nombre_sin_ext + ".ogg"

    if os.path.exists(ruta_salida):
        print(f"Ya existe: {ruta_salida}")
        return

    try:
        subprocess.run([
            "ffmpeg",
            "-i", ruta_archivo,
            "-acodec", "libvorbis",  # Códec para OGG
            ruta_salida
        ], check=True)
        print(f"✅ Convertido: {ruta_archivo} → {ruta_salida}")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al convertir {ruta_archivo}: {e}")

def procesar_carpeta(carpeta):
    for carpeta_actual, _, archivos in os.walk(carpeta):
        for archivo in archivos:
            if archivo.lower().endswith(AUDIO_FORMATOS):
                ruta_completa = os.path.join(carpeta_actual, archivo)
                convertir_a_ogg(ruta_completa)

if __name__ == "__main__":
    carpeta = input("🔍 Pega la ruta de la carpeta que contiene los audios:\n> ").strip('"')
    if os.path.isdir(carpeta):
        procesar_carpeta(carpeta)
    else:
        print("❌ Ruta inválida o la carpeta no existe.")
