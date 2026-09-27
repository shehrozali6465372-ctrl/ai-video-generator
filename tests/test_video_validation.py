from pathlib import Path
from unittest.mock import patch

import pytest

from video_validation import validate_video_output


def test_missing_output_rejected(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="missing"):
        validate_video_output(tmp_path / "missing.mp4")


def test_empty_output_rejected(tmp_path: Path) -> None:
    output = tmp_path / "empty.mp4"
    output.touch()
    with pytest.raises(RuntimeError, match="empty"):
        validate_video_output(output)


def test_invalid_mp4_rejected(tmp_path: Path) -> None:
    output = tmp_path / "invalid.mp4"
    output.write_bytes(b"not-a-video")
    completed = type("Completed", (), {"returncode": 1})()
    with patch("video_validation.imageio_ffmpeg.get_ffmpeg_exe", return_value="ffmpeg"):
        with patch("video_validation.subprocess.run", return_value=completed):
            with pytest.raises(RuntimeError, match="integrity"):
                validate_video_output(output)


def test_valid_probe_accepted(tmp_path: Path) -> None:
    output = tmp_path / "valid.mp4"
    output.write_bytes(b"placeholder")
    completed = type("Completed", (), {"returncode": 0})()
    with patch("video_validation.imageio_ffmpeg.get_ffmpeg_exe", return_value="ffmpeg"):
        with patch("video_validation.subprocess.run", return_value=completed):
            validate_video_output(output)
