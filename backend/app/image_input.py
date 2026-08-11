from __future__ import annotations

import base64
import binascii
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_SCAN_DIR = BACKEND_ROOT / "runtime_scans"

MAX_IMAGE_SIZE_BYTES = 10 * 1024 * 1024

ALLOWED_MIME_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}


@dataclass(frozen=True)
class DecodedImage:
    mime_type: str
    extension: str
    size_bytes: int
    saved_path: Path


def decode_and_save_data_url(image_data_url: str) -> DecodedImage:
    if "," not in image_data_url:
        raise ValueError("Invalid data URL format.")

    header, encoded_data = image_data_url.split(",", 1)

    if not header.startswith("data:image/"):
        raise ValueError("image_data_url must start with data:image/.")

    if ";base64" not in header:
        raise ValueError("image_data_url must be base64 encoded.")

    mime_type = header.replace("data:", "").replace(";base64", "").strip()

    if mime_type not in ALLOWED_MIME_TYPES:
        raise ValueError(f"Unsupported image MIME type: {mime_type}")

    try:
        image_bytes = base64.b64decode(encoded_data, validate=True)
    except binascii.Error as error:
        raise ValueError("image_data_url contains invalid base64 data.") from error

    if not image_bytes:
        raise ValueError("Decoded image is empty.")

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise ValueError("Decoded image exceeds maximum size of 10 MB.")

    extension = ALLOWED_MIME_TYPES[mime_type]
    RUNTIME_SCAN_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_path = RUNTIME_SCAN_DIR / f"latest_scan_{timestamp}{extension}"
    saved_path.write_bytes(image_bytes)

    return DecodedImage(
        mime_type=mime_type,
        extension=extension,
        size_bytes=len(image_bytes),
        saved_path=saved_path,
    )


def to_backend_relative_path(path: Path) -> str:
    try:
        return path.relative_to(BACKEND_ROOT).as_posix()
    except ValueError:
        return path.as_posix()