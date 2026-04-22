# THIS PROJECT IS ON BETA YET - Be careful

🎧 OMEGA Audio Converter (Unified Suite)

**Language:** 🇬🇧 English | 🇪🇸 [Español](README.md)

> **A professional desktop suite for massive conversion, compression and audio wave visualization, optimized for OGG Vorbis (Video Games and Web).**

**OMEGA Audio Converter** is the definitive evolution of the old _Audio Toolkit_. It merges 4 independent tools into a single modern graphical interface. Designed for developers and content creators, this tool allows you to visualize how audio behaves, predict its final weight and convert entire libraries to lightweight formats in seconds.

![1769445521124](images/README/1769445521124.png)

## ✨ Star Features

- **🌊 Reactive Waveform Viewer:** Visually inspect the peaks and silences of each audio track. The drawing is generated in the background (Multithreading) to ensure the interface never freezes, even with 1-hour audio.
- **🧠 Real-Time Predictive Calculator:** As you adjust the quality slider (Bitrate), the system instantly recalculates the estimated weight of the final file and shows you the exact percentage of disk savings.
- **⚡ Universal Converter:** Drag MP3, WAV, FLAC, M4A or AAC files and unify them to the royalty-free standard **OGG Vorbis**.
- **🗂️ Auto-Organizer:** Enable the "Organize in subfolders" option and the script will automatically create `/ogg` folders so your resources don't mix with the originals.
- **🔉 Channel Control:** Your web audio doesn't need surround sound? Force Stereo to Mono conversion with one click to cut the weight in half without touching the bitrate.

---

## ⚙️ Requirements and Installation

The script features an **Auto-Installer** for its Python dependencies (Pydub, Pillow, TTKBootstrap). However, it requires an external audio engine.

**Mandatory Requirement:**

- **FFmpeg:** Must be installed and added to your system's Environment Variables (PATH). If you don't have it, check the [FFmpeg Installation Guide](INSTALL_FFMPEG.en.md).

### Execution

```bash
python omega_audio_converter.py
```

## 📖 Usage Guide

**Load Audio:** Use the ➕ Add button to load your sound effects or music tracks.

**Inspect:** Click on any element in the list. You'll see its waveform in the Inspector and its original data (weight, duration, bitrate).

**Calibrate Quality:**

Adjust the "Quality (Bitrate)" slider.

- For Web/FX: 96 kbps to 128 kbps is the golden standard (good sound, low weight).
- For High-Fidelity Music: 192 kbps to 320 kbps.

**Process:** Choose your output folder and press 🚀 PROCESS COMPLETE BATCH.

## 📈 Project Evolution (Changelog)

This suite replaces and unifies the following old terminal scripts (CLI):

🗑️ converter-ogg.py (Now integrated as base engine).

🗑️ separate-ogg-files.py (Now integrated as the "Auto-Organizer").

🗑️ ogg-compressor.py and ogg-compressor-max.py (Replaced by the Dynamic Predictive Calculator).

**Benefit:** You no longer have to guess what bitrate to use so the audio weighs less than 1MB; the software does the calculation for you visually before exporting.

## ⚖️ License and Credits

This project uses open source Python libraries and the powerful FFmpeg multimedia processing engine.

Developed for massive asset optimization in engines like Godot, Unity, Unreal Engine and Web Development.
