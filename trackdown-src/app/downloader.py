import os
import subprocess
from pathlib import Path

def download_track(url, bitrate, fmt, folder, log_callback=None):
    folder = Path(folder).expanduser()
    folder.mkdir(parents=True, exist_ok=True)

    output_template = str(
        folder / "{artist}/{track-number:02d} - {title}.{output-ext}"
    )

    command = [
        "spotdl", "download", url,
        "--bitrate", bitrate,
        "--format", fmt,
        "--lyrics", "genius",
        "--preload",
        "--output", output_template
    ]

    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )

    for line in process.stdout:
        if log_callback:
            log_callback(line.strip())

    process.wait()

    if process.returncode != 0:
        raise RuntimeError("Download failed")
