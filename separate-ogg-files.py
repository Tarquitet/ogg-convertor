import os
import shutil

# Tipos de audio reconocidos
AUDIO_FORMATOS = (".mp3", ".wav", ".flac", ".aac", ".m4a", ".ogg")

def organizar_por_extension(carpeta_base):
    for raiz, _, archivos in os.walk(carpeta_base):
        for archivo in archivos:
            extension = os.path.splitext(archivo)[1].lower()
            if extension in AUDIO_FORMATOS:
                ruta_actual = os.path.join(raiz, archivo)
                subcarpeta_destino = os.path.join(raiz, extension[1:])  # sin el punto

                if not os.path.exists(subcarpeta_destino):
                    os.makedirs(subcarpeta_destino)

                nuevo_destino = os.path.join(subcarpeta_destino, archivo)

                # Evita sobrescribir si ya existe en destino
                if os.path.abspath(ruta_actual) != os.path.abspath(nuevo_destino):
                    try:
                        shutil.move(ruta_actual, nuevo_destino)
                        print(f"✅ Movido: {archivo} → {subcarpeta_destino}")
                    except Exception as e:
                        print(f"❌ Error moviendo {archivo}: {e}")

if __name__ == "__main__":
    carpeta = input("📂 Pega la ruta de la carpeta donde están los audios mezclados:\n> ").strip('"')
    if os.path.isdir(carpeta):
        organizar_por_extension(carpeta)
        print("\n🎉 Archivos organizados por tipo de audio.")
    else:
        print("❌ Ruta inválida o la carpeta no existe.")
