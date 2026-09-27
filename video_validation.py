from __future__ import annotations

import subprocess
from pathlib import Path

import imageio_ffmpeg

MAX_VIDEO_BYTES = 500 * 1024 * 1024


def validate_video_output(path: Path) -> None:
    if not path.is_file():
        raise RuntimeError("Video output file is missing.")
    size = path.stat().st_size
    if size <= 0:
        raise RuntimeError("Video output file is empty.")
    if size > MAX_VIDEO_BYTES:
        raise RuntimeError("Video output exceeds the maximum allowed size.")

    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    result = subprocess.run(
        [ffmpeg, "-v", "error", "-i", str(path), "-f", "null", "-"],
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Generated video failed MP4 integrity validation.")
