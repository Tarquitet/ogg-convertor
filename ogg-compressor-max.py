import os
from pydub import AudioSegment
from pydub.utils import mediainfo

# Configuración
MAX_SIZE_MB = 1
MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024
DEFAULT_BITRATE = 1411000  # 1411 kbps
MIN_VALID_BITRATE = 48000  # 48 kbps mínimo válido para Vorbis

def calcular_bitrate_para_1mb(duracion_segundos):
    """Calcula el bitrate máximo en bps para que pese menos de 1MB."""
    return int((MAX_SIZE_BYTES * 8) / duracion_segundos)

def main():
    print("🎧 Compresor de archivos .ogg (objetivo: < 1 MB, sin perder calidad)")
    
    carpeta_entrada = input("📁 Ingresa la ruta de la carpeta de entrada: ").strip('"')
    carpeta_salida = input("📁 Ingresa la ruta donde guardar los archivos comprimidos: ").strip('"')

    if not os.path.exists(carpeta_entrada):
        print("❌ La carpeta de entrada no existe.")
        return

    for ruta_actual, _, archivos in os.walk(carpeta_entrada):
        for archivo in archivos:
            if archivo.lower().endswith(".ogg"):
                ruta_origen = os.path.join(ruta_actual, archivo)

                try:
                    audio = AudioSegment.from_ogg(ruta_origen)
                    duracion = len(audio) / 1000.0  # en segundos

                    try:
                        info = mediainfo(ruta_origen)
                        bitrate_original = int(info.get("bit_rate", DEFAULT_BITRATE))
                    except:
                        bitrate_original = DEFAULT_BITRATE

                    bitrate_limite = calcular_bitrate_para_1mb(duracion)
                    target_bitrate = min(bitrate_limite, int(bitrate_original * 0.75))

                    if target_bitrate < MIN_VALID_BITRATE:
                        print(f"⚠️ Bitrate muy bajo para '{archivo}', ajustando a {MIN_VALID_BITRATE // 1000} kbps.")
                        target_bitrate = MIN_VALID_BITRATE

                    relativa = os.path.relpath(ruta_actual, carpeta_entrada)
                    carpeta_destino = os.path.join(carpeta_salida, relativa)
                    os.makedirs(carpeta_destino, exist_ok=True)
                    ruta_salida = os.path.join(carpeta_destino, archivo)

                    audio.export(ruta_salida, format="ogg", bitrate=f"{int(target_bitrate / 1000)}k")
                    print(f"✔️ {archivo} → {int(target_bitrate / 1000)} kbps | Guardado en: {ruta_salida}")

                except Exception as e:
                    print(f"❌ Error al procesar '{archivo}': {e}")

if __name__ == "__main__":
    main()
