# YouTube Downloader CLI
![Static Badge](https://img.shields.io/badge/python-python?style=for-the-badge&logo=python&logoColor=%23fefefe&color=%233776AB) ![Static Badge](https://img.shields.io/badge/env-env?style=for-the-badge&logo=dotenv&logoColor=%23333&color=%23ECD53F) ![Static Badge](https://img.shields.io/badge/pydantic-pydantic?style=for-the-badge&logo=pydantic&logoColor=%23fefefe&color=%23E92063) ![Static Badge](https://img.shields.io/badge/youtube-youtube?style=for-the-badge&logo=youtube&logoColor=%23fefefe&color=%23FF0000)

A command-line interface (CLI) tool for downloading YouTube videos and playlists with ease, supporting resolution selection, output format conversion, and automatic handling of age-restricted content via browser cookies.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
   * [Basic Download](#basic-download)
   * [Age-Restricted Videos](#age-restricted-videos)
7. [Command-Line Arguments](#command-line-arguments)
8. [Environment Variables](#environment-variables)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

---

## Overview

The YouTube Downloader CLI is a robust Python-based utility built on top of [yt-dlp](https://github.com/yt-dlp/yt-dlp) and [FFmpeg](https://ffmpeg.org/). It provides an interactive command-line experience for:

* Downloading single YouTube videos or entire playlists
* Choosing video quality (up to 1080p or higher if available)
* Converting or packaging downloads in `mkv` or `mp4` formats via FFmpeg
* Automatically retrying downloads with browser cookies to bypass age restrictions

This tool is ideal for users who require a simple yet powerful CLI wrapper to manage downloads and handle edge cases like age verification seamlessly.

---

## Features

* **Interactive Prompts**: Easily input URLs, choose quality, and set output formats via guided prompts.
* **Playlist Support**: Detects if a URL is a playlist and organizes downloads into a named subfolder.
* **Quality Mapping**: Predefined options:

  * Best available
  * Above High (1080p)
  * High (720p)
  * Medium (1440p)
  * Low (≤480p)
* **Output Formats**: `.mkv` or `.mp4`, with FFmpeg post-processing for container conversion.
* **Age Restriction Handling**: On encountering an age-verification or login error, automatically detects installed browsers (Firefox, Chrome, Chromium, Edge, Brave) and retries with `--cookies-from-browser`.
* **Resumable Downloads**: Monitors network connectivity; upon disconnect, waits and resumes when online.
* **Graceful Error Handling**: Handles missing folders, permission issues, and user interrupts.

---

## Prerequisites

Ensure the following are installed on your system:

1. **Python 3.8+**
2. **yt-dlp**

   ```bash
   pip install yt-dlp
   ```
3. **FFmpeg**

   * macOS: `brew install ffmpeg`
   * Ubuntu/Debian: `sudo apt install ffmpeg`
   * Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html), add to PATH
4. **Python Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   This includes:

   * `inquirer`
   * `python-dotenv`
   * `yt-dlp`
   * Custom decorators (`timed`, `ffmpeg_required`, `network_required`)

---

## Installation

1. **Clone the `CLI` branch**

   ```bash
   git clone --branch CLI https://github.com/S1mon009/YouTube-downloader.git
   cd YouTube-downloader
   ```
2. **Create and activate virtual environment** (optional but recommended)

   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   venv\Scripts\activate    # Windows
   ```
3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Environment File**: Create a `.env` in the project root to override defaults:

   ```ini
   # .env
   DOWNLOAD_FOLDER=/path/to/downloads
   ```
2. **Custom Cookies File** (optional): If you prefer a manual cookies file instead of browser integration, modify the `run_yt_dlp_with_cookies()` method to insert `--cookies path/to/cookies.txt`.

---

## Usage

Run the main script:

```bash
python main.py
```

### Basic Download

1. **Enter URL**: Paste a YouTube video or playlist link.
2. **Confirm Path**: Accept or change the default download folder.
3. **Select Quality**: Choose one of the predefined quality presets.
4. **Select Format**: Choose between `mkv` or `mp4`.
5. **Confirm and Download**: Review summary and confirm to start.

### Age-Restricted Videos

If a video requires age verification:

1. The CLI detects the error.
2. It automatically scans for installed browsers.
3. Retries download with `--cookies-from-browser <browser>`.
4. Falls back to plain download if no supported browser is found.

---

## Command-Line Arguments

> **Note:** Currently, the tool is interactive.
> Future enhancements may include direct flags (e.g., `--url`, `--quality`, `--format`).

---

## Environment Variables

* `DOWNLOAD_FOLDER`: Override the default download directory.

---

## Troubleshooting

* **`FileNotFoundError`**: Ensure `DOWNLOAD_FOLDER` exists or create it via prompt.
* **`PermissionError`**: Adjust directory permissions or choose another folder.
* **`KeyboardInterrupt`**: Use `Ctrl+C` to cancel anytime; partial downloads may remain.
* **Missing Browser**: Install one of Firefox, Chrome, Chromium, Edge, Brave for age-restriction support.

---

## Contributing

1. Fork this repo and checkout the `CLI` branch.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Commit changes with Conventional Commits.
4. Push and open a pull request against `CLI`.
