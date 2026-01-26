import os
import subprocess

def obtener_bitrate_original(ruta_ogg):
    try:
        resultado = subprocess.run([
            "ffprobe", "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=bit_rate",
            "-of", "default=noprint_wrappers=1:nokey=1",
            ruta_ogg
        ], capture_output=True, text=True)

        bitrate_str = resultado.stdout.strip()
        if bitrate_str:
            return int(bitrate_str)
        else:
            return None
    except Exception:
        return None

def recomprimir_ogg(ruta_ogg, ruta_destino):
    bitrate_original = obtener_bitrate_original(ruta_ogg)

    if not bitrate_original:
        print(f"❌ No se pudo obtener bitrate de: {ruta_ogg}")
        return

    # Calcular nuevo bitrate (~50%)
    nuevo_bitrate_kbps = max(int(bitrate_original * 0.5 / 1000), 32)  # no menos de 32 kbps
    nuevo_bitrate_str = f"{nuevo_bitrate_kbps}k"

    if not os.path.exists(os.path.dirname(ruta_destino)):
        os.makedirs(os.path.dirname(ruta_destino))

    try:
        subprocess.run([
            "ffmpeg",
            "-y",  # sobrescribe si existe
            "-i", ruta_ogg,
            "-acodec", "libvorbis",
            "-b:a", nuevo_bitrate_str,
            ruta_destino
        ], check=True)
        print(f"✅ {os.path.basename(ruta_ogg)} comprimido a {nuevo_bitrate_str}")
    except subprocess.CalledProcessError:
        print(f"❌ Error al recomprimir: {ruta_ogg}")

def comprimir_oggs(origen, destino):
    for raiz, _, archivos in os.walk(origen):
        for archivo in archivos:
            if archivo.lower().endswith(".ogg"):
                ruta_ogg = os.path.join(raiz, archivo)

                # Calcula ruta relativa para copiar estructura
                ruta_relativa = os.path.relpath(raiz, origen)
                ruta_destino = os.path.join(destino, ruta_relativa, archivo)

                recomprimir_ogg(ruta_ogg, ruta_destino)

if __name__ == "__main__":
    origen = input("📂 Ruta de la carpeta de origen (ogg sin comprimir):\n> ").strip('"')
    destino = input("📁 Ruta de la carpeta destino para guardar los .ogg comprimidos:\n> ").strip('"')

    if os.path.isdir(origen):
        comprimir_oggs(origen, destino)
        print("\n🎉 Compresión terminada con estructura replicada.")
    else:
        print("❌ La ruta de origen no es válida.")
