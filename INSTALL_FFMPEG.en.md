# 🛠️ FFmpeg Installation Guide

**Language:** 🇬🇧 English | 🇪🇸 [Español](INSTALL_FFMPEG.md)

The scripts in this toolkit depend on **FFmpeg**, a free and open-source tool for processing audio and video.

If when running the scripts you get the error: `FileNotFoundError: [WinError 2]`, it means FFmpeg is not installed or not in your system's PATH. Follow these steps according to your operating system:

---

## 🪟 For Windows Users

### Step 1: Download

1. Go to the official page: [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Hover over the Windows logo and click on one of the build links (e.g., _gyan.dev_ or _BtbN_).
3. Download the `.zip` file of the "Release" or "Master" version.

### Step 2: Extract

1. Create a folder on your C: drive called `FFmpeg` (Path: `C:\FFmpeg`).
2. Extract the contents of the `.zip` inside that folder.
3. Make sure the `ffmpeg.exe` file is located at `C:\FFmpeg\bin\ffmpeg.exe`.

### Step 3: Add to PATH (Important!)

For Python to "see" FFmpeg, you must add it to Windows environment variables:

1. Press the `Windows` key and search for **"Environment Variables"** (or "Variables de entorno").
2. Click the **"Environment Variables..."** button in the bottom right.
3. In the "System variables" section (below), find the variable called `Path`, select it and click **Edit**.
4. Click **New** and paste the path to your bin folder: `C:\FFmpeg\bin`
5. Click **OK** in all windows.

_(Note: You will need to close and reopen any CMD terminal or VS Code you had open for the changes to take effect)._

---

## 🍏 For macOS (Mac) Users

The easiest way is to use Homebrew. Open your Terminal and run:

```bash
brew install ffmpeg
```

## 🐧 For Linux Users

Open your terminal and run the command according to your distribution:

**Ubuntu / Debian:**

```bash
sudo apt update && sudo apt install ffmpeg
```

**Arch Linux:**

```bash
sudo pacman -S ffmpeg
```

## ✅ Verify Installation

To check that everything is ready, open a terminal (CMD, PowerShell or Terminal) and type:

```bash
ffmpeg -version
```

If you see a long text with the version and configuration details, you're ready to use the OGG Toolkit!
