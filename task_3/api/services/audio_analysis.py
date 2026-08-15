import json
import re
import subprocess
import tempfile
import os

from fastapi import HTTPException


def analyze_audio(audio_file):
    """
    Analyze uploaded audio using ffprobe + ffmpeg.

    Returns:
        duration_seconds
        sample_rate_khz
        bitrate_kbps
        loudness_db
    """

    temp_path = None

    try:

        # -----------------------------------------
        # Save UploadFile to temporary file
        # -----------------------------------------

        suffix = os.path.splitext(audio_file.filename or "")[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_path = temp_file.name

            audio_file.file.seek(0)

            while True:
                chunk = audio_file.file.read(1024 * 1024)

                if not chunk:
                    break

                temp_file.write(chunk)

        # -----------------------------------------
        # Duration + sample rate + bitrate
        # -----------------------------------------

        probe_command = [
            "ffprobe",
            "-v", "error",
            "-show_entries",
            "format=duration,bit_rate",
            "-show_entries",
            "stream=sample_rate,bit_rate",
            "-of", "json",
            temp_path
        ]

        probe_result = subprocess.run(
            probe_command,
            capture_output=True,
            text=True
        )

        if probe_result.returncode != 0:
            raise Exception(probe_result.stderr)

        probe_data = json.loads(probe_result.stdout)

        # -----------------------------------------
        # Duration
        # -----------------------------------------

        duration = None

        format_data = probe_data.get("format", {})

        if format_data.get("duration"):
            duration = float(format_data["duration"])

        # -----------------------------------------
        # Sample rate
        # -----------------------------------------

        sample_rate = None

        streams = probe_data.get("streams", [])

        for stream in streams:

            if stream.get("sample_rate"):

                sample_rate = float(
                    stream["sample_rate"]
                )

                break

        # Convert Hz → kHz

        sample_rate_khz = (
            sample_rate / 1000
            if sample_rate
            else None
        )

        # -----------------------------------------
        # Bitrate
        # -----------------------------------------

        bitrate = None

        # Try audio stream bitrate first

        for stream in streams:

            if stream.get("bit_rate"):

                bitrate = float(
                    stream["bit_rate"]
                )

                break

        # Otherwise use format bitrate

        if bitrate is None and format_data.get("bit_rate"):

            bitrate = float(
                format_data["bit_rate"]
            )

        bitrate_kbps = (
            bitrate / 1000
            if bitrate
            else None
        )

        # -----------------------------------------
        # Loudness
        # -----------------------------------------

        loudness_command = [
            "ffmpeg",
            "-i", temp_path,
            "-af", "ebur128=peak=true",
            "-f", "null",
            "-"
        ]

        loudness_result = subprocess.run(
            loudness_command,
            capture_output=True,
            text=True
        )

        # FFmpeg writes ebur128 output to stderr

        loudness_output = loudness_result.stderr

        loudness_db = None

        # Look for:
        # I: -18.4 LUFS

        matches = re.findall(
            r"I:\s*(-?\d+(?:\.\d+)?)\s+LUFS",
            loudness_output
        )

        if matches:

            loudness_db = float(matches[-1])

        return {
            "duration_seconds": duration,
            "sample_rate_khz": sample_rate_khz,
            "bitrate_kbps": bitrate_kbps,
            "loudness_db": loudness_db
        }

    except FileNotFoundError:

        raise HTTPException(
            status_code=500,
            detail="FFmpeg/FFprobe is not installed or not available in PATH"
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Audio analysis failed: {str(e)}"
        )

    finally:

        if temp_path and os.path.exists(temp_path):

            os.remove(temp_path)