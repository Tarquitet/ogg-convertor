"""
OMEGA AUDIO CONVERTER (Unified Toolkit)
Convierte, comprime y visualiza ondas de audio para desarrollo web y videojuegos.
Requiere: FFmpeg instalado en el sistema.
"""
import sys
import os
import subprocess
import threading
import io
import math
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox

# --- 1. AUTO-INSTALADOR DE DEPENDENCIAS ---
def setup_dependencies():
    required_libs = {
        'ttkbootstrap': 'ttkbootstrap',
        'pydub': 'pydub',
        'Pillow': 'PIL'
    }
    installed = False
    for package, import_name in required_libs.items():
        try:
            __import__(import_name)
        except ImportError:
            print(f"[SISTEMA] Instalando {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                installed = True
            except: pass
    if installed: os.execv(sys.executable, ['python'] + sys.argv)

setup_dependencies()

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pydub import AudioSegment
from pydub.utils import mediainfo

# --- VERIFICACIÓN DE FFMPEG ---
if not shutil.which("ffmpeg"):
    import tkinter.messagebox as msg
    root = tk.Tk()
    root.withdraw()
    msg.showerror("Error Crítico", "FFmpeg no está instalado o no está en el PATH de Windows.\n\nEs obligatorio para procesar audio.")
    sys.exit()

# --- CONSTANTES ---
AUDIO_EXT = ('.mp3', '.wav', '.flac', '.aac', '.m4a', '.ogg')

class AudioItem:
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.ext = os.path.splitext(self.name)[1].lower()
        self.size_bytes = os.path.getsize(path)
        self.duration_sec = 0.0
        self.original_bitrate = 0
        self.audio_segment = None
        self.waveform_data = [] # Picos normalizados

class OmegaAudioGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OMEGA Audio Converter & Inspector")
        self.root.geometry("1100x700")
        
        self.items = []
        self.current_item = None
        self.out_dir = tk.StringVar(value=os.path.join(os.getcwd(), "output_audio"))

        # Variables de Control
        self.var_bitrate = tk.IntVar(value=96)
        self.var_channels = tk.StringVar(value="2") # 1 = Mono, 2 = Stereo
        self.var_organize = tk.BooleanVar(value=True) # Crear subcarpetas por extensión

        self.setup_ui()

    def setup_ui(self):
        # Barra superior
        top_frame = ttk.Frame(self.root, padding=10)
        top_frame.pack(fill="x")
        ttk.Button(top_frame, text="➕ Agregar Carpeta/Archivos", command=self.add_files, bootstyle=SUCCESS).pack(side="left", padx=5)
        ttk.Button(top_frame, text="🗑️ Limpiar", command=self.clear_list, bootstyle=DANGER).pack(side="left", padx=5)

        # Contenedor Principal
        main_frame = ttk.PanedWindow(self.root, orient="horizontal")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Panel Izquierdo: Lista
        left_frame = ttk.Frame(main_frame)
        main_frame.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Lista de Audios", font=("Arial", 12, "bold")).pack(anchor="w")
        self.listbox = tk.Listbox(left_frame, font=("Arial", 10), bg="#222", fg="#fff", selectbackground="#007acc")
        self.listbox.pack(fill="both", expand=True, pady=5)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

        # Panel Derecho: Inspector y Controles
        right_frame = ttk.Frame(main_frame)
        main_frame.add(right_frame, weight=3)

        # --- WAVEFORM CANVAS ---
        ttk.Label(right_frame, text="Inspector de Forma de Onda", font=("Arial", 12, "bold")).pack(anchor="w")
        self.canvas = tk.Canvas(right_frame, height=150, bg="#111", highlightthickness=0)
        self.canvas.pack(fill="x", pady=10)

        # --- INFO HUD ---
        self.lbl_info = ttk.Label(right_frame, text="Selecciona un audio para inspeccionar", font=("Consolas", 11), bootstyle=INFO)
        self.lbl_info.pack(fill="x", pady=5)
        
        self.lbl_savings = ttk.Label(right_frame, text="", font=("Arial", 14, "bold"), foreground="green")
        self.lbl_savings.pack(fill="x", pady=5)

        # --- CONTROLES DE COMPRESIÓN ---
        ctrl_frame = ttk.LabelFrame(right_frame, text="Ajustes de Compresión (OGG Vorbis)", padding=15)
        ctrl_frame.pack(fill="x", pady=10)

        # Slider de Bitrate
        row1 = ttk.Frame(ctrl_frame)
        row1.pack(fill="x", pady=5)
        ttk.Label(row1, text="Calidad (Bitrate kbps):", width=20).pack(side="left")
        self.lbl_bitrate_val = ttk.Label(row1, text="96 kbps", font=("Arial", 10, "bold"), width=8)
        self.lbl_bitrate_val.pack(side="right")
        self.slider_bitrate = ttk.Scale(row1, from_=32, to=320, variable=self.var_bitrate, command=self.update_estimation)
        self.slider_bitrate.pack(fill="x", expand=True, padx=10)

        # Canales y Extras
        row2 = ttk.Frame(ctrl_frame)
        row2.pack(fill="x", pady=10)
        ttk.Label(row2, text="Canales:").pack(side="left")
        ttk.Radiobutton(row2, text="Estéreo (2.0)", variable=self.var_channels, value="2", command=self.update_estimation).pack(side="left", padx=10)
        ttk.Radiobutton(row2, text="Mono (Unificar)", variable=self.var_channels, value="1", command=self.update_estimation).pack(side="left", padx=5)
        ttk.Checkbutton(row2, text="Organizar en subcarpetas (/ogg, /mp3)", variable=self.var_organize, bootstyle="round-toggle").pack(side="right")

        # --- EXPORTAR ---
        export_frame = ttk.LabelFrame(right_frame, text="Exportar", padding=15)
        export_frame.pack(fill="x", pady=10)
        
        out_row = ttk.Frame(export_frame)
        out_row.pack(fill="x", pady=5)
        ttk.Label(out_row, text="Carpeta de Salida:").pack(side="left")
        ttk.Entry(out_row, textvariable=self.out_dir).pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(out_row, text="Examinar...", command=self.choose_dir).pack(side="left")

        ttk.Button(export_frame, text="🚀 PROCESAR LOTE COMPLETO", bootstyle=SUCCESS, command=self.process_batch).pack(fill="x", pady=15)

    def choose_dir(self):
        d = filedialog.askdirectory()
        if d: self.out_dir.set(d)

    def clear_list(self):
        self.items.clear()
        self.listbox.delete(0, tk.END)
        self.canvas.delete("all")
        self.lbl_info.config(text="")
        self.lbl_savings.config(text="")

    def add_files(self):
        paths = filedialog.askopenfilenames(filetypes=[("Audio Files", "*.mp3 *.wav *.ogg *.flac *.m4a *.aac")])
        for p in paths:
            if not any(i.path == p for i in self.items):
                item = AudioItem(p)
                self.items.append(item)
                self.listbox.insert(tk.END, item.name)

    def format_size(self, size_bytes):
        if size_bytes < 1024 * 1024: return f"{size_bytes / 1024:.2f} KB"
        return f"{size_bytes / (1024 * 1024):.2f} MB"

    def format_time(self, seconds):
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02}:{secs:02}"

    def on_select(self, event):
        idx = self.listbox.curselection()
        if not idx: return
        self.current_item = self.items[idx[0]]
        
        self.lbl_info.config(text=f"Cargando análisis para: {self.current_item.name} ...")
        threading.Thread(target=self.analyze_audio, args=(self.current_item,), daemon=True).start()

    def analyze_audio(self, item):
        """Carga el audio en segundo plano para no congelar la GUI"""
        try:
            # 1. Metadatos rápidos
            info = mediainfo(item.path)
            item.original_bitrate = int(info.get("bit_rate", 0)) // 1000 # a kbps
            item.duration_sec = float(info.get("duration", 0))

            # 2. Carga pesada para la forma de onda
            if item.audio_segment is None:
                item.audio_segment = AudioSegment.from_file(item.path)
                
                # Obtener picos para el dibujo (Downsampling a 800 puntos)
                samples = item.audio_segment.get_array_of_samples()
                step = max(1, len(samples) // 800)
                # Tomamos valor absoluto del pico en ese chunk
                item.waveform_data = [max(abs(s) for s in samples[i:i+step]) for i in range(0, len(samples), step)]

            self.root.after(0, lambda: self.update_gui_after_analysis(item))
        except Exception as e:
            self.root.after(0, lambda: self.lbl_info.config(text=f"Error cargando audio: {e}", bootstyle=DANGER))

    def update_gui_after_analysis(self, item):
        if self.current_item != item: return # Usuario cambió de selección rápido
        
        # Info Textual
        orig_size = self.format_size(item.size_bytes)
        dur = self.format_time(item.duration_sec)
        kbps = item.original_bitrate or "N/A"
        
        info_str = f"Formato: {item.ext.upper()[1:]} | Duración: {dur} | Peso Orig: {orig_size} | Bitrate Orig: {kbps} kbps"
        self.lbl_info.config(text=info_str)

        # Dibujar Onda
        self.draw_waveform(item)
        self.update_estimation()

    def draw_waveform(self, item):
        self.canvas.delete("all")
        if not item.waveform_data: return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        max_val = max(item.waveform_data) if max(item.waveform_data) > 0 else 1
        
        # Estética de la onda
        mid_y = height / 2
        bar_width = width / len(item.waveform_data)

        for i, val in enumerate(item.waveform_data):
            x = i * bar_width
            # Escalar el pico a la altura del canvas
            h = (val / max_val) * mid_y
            # Dibujar línea simétrica (arriba y abajo)
            color = "#00ff88" if item.ext == ".ogg" else "#00bfff"
            self.canvas.create_line(x, mid_y - h, x, mid_y + h, fill=color, width=1.5)

    def update_estimation(self, *args):
        if not self.current_item or not self.current_item.duration_sec: return
        
        target_kbps = self.var_bitrate.get()
        self.lbl_bitrate_val.config(text=f"{target_kbps} kbps")

        # Cálculo de peso estimado: (Bitrate en bits * segundos) / 8 = Bytes
        est_bytes = (target_kbps * 1000 * self.current_item.duration_sec) / 8
        orig_bytes = self.current_item.size_bytes

        savings_percent = 100 - ((est_bytes / orig_bytes) * 100)
        
        msg = f"Peso Estimado: {self.format_size(est_bytes)} "
        if savings_percent > 0:
            msg += f" (Ahorras {savings_percent:.1f}%)"
            self.lbl_savings.config(text=msg, foreground="#00ff88")
        else:
            msg += f" (El archivo pesará MÁS que el original)"
            self.lbl_savings.config(text=msg, foreground="red")

    def process_batch(self):
        if not self.items: return
        
        out_dir = self.out_dir.get()
        if not os.path.exists(out_dir): os.makedirs(out_dir)

        # Ventana de Progreso
        prog_win = tk.Toplevel(self.root)
        prog_win.title("Procesando Audios...")
        prog_win.geometry("400x150")
        
        lbl_status = ttk.Label(prog_win, text="Iniciando...", font=("Arial", 10))
        lbl_status.pack(pady=10)
        p_bar = ttk.Progressbar(prog_win, maximum=len(self.items))
        p_bar.pack(fill="x", padx=20, pady=10)

        target_kbps = self.var_bitrate.get()
        channels = self.var_channels.get()
        organize = self.var_organize.get()

        def worker():
            success = 0
            for i, item in enumerate(self.items):
                lbl_status.config(text=f"Convirtiendo: {item.name}")
                prog_win.update()

                # Definir subcarpetas si está activado
                dest_dir = out_dir
                if organize:
                    dest_dir = os.path.join(out_dir, "ogg")
                    if not os.path.exists(dest_dir): os.makedirs(dest_dir)

                base_name = os.path.splitext(item.name)[0]
                out_path = os.path.join(dest_dir, f"{base_name}.ogg")

                # Comando FFmpeg para OGG Vorbis
                cmd = [
                    "ffmpeg", "-y", "-i", item.path,
                    "-acodec", "libvorbis",
                    "-b:a", f"{target_kbps}k",
                    "-ac", channels,
                    out_path
                ]

                try:
                    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    success += 1
                except Exception as e:
                    print(f"Error en {item.name}: {e}")

                p_bar['value'] = i + 1
                prog_win.update()

            prog_win.destroy()
            messagebox.showinfo("Completado", f"Proceso Finalizado.\nÉxito: {success} de {len(self.items)}")

        threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")
    OmegaAudioGUI(app)
    app.mainloop()