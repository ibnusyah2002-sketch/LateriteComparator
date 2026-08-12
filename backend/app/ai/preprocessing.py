from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageOps


PREPROCESSING_METHOD = "center_crop_autocontrast_v1"
DEFAULT_CENTER_CROP_RATIO = 0.72
DEFAULT_MAX_SIZE = 768

BACKEND_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_SCAN_DIR = BACKEND_ROOT / "runtime_scans"


@dataclass(frozen=True)
class PreprocessedImage:
    original_path: Path
    processed_path: Path
    method: str
    crop_ratio: float
    original_size: tuple[int, int]
    processed_size: tuple[int, int]


def preprocess_scan_image(
    image_path: Path,
    crop_ratio: float = DEFAULT_CENTER_CROP_RATIO,
    max_size: int = DEFAULT_MAX_SIZE,
) -> PreprocessedImage:
    if not image_path.exists():
        raise FileNotFoundError(f"Scan image not found: {image_path}")

    if crop_ratio <= 0 or crop_ratio > 1:
        raise ValueError("crop_ratio must be greater than 0 and less than or equal to 1.")

    RUNTIME_SCAN_DIR.mkdir(parents=True, exist_ok=True)

    with Image.open(image_path) as image:
        rgb_image = image.convert("RGB")
        original_size = rgb_image.size

        cropped_image = center_crop(rgb_image, crop_ratio=crop_ratio)
        normalized_image = ImageOps.autocontrast(cropped_image, cutoff=1)

        normalized_image.thumbnail((max_size, max_size))

        processed_path = build_processed_path(image_path)
        normalized_image.save(processed_path, format="JPEG", quality=90, optimize=True)

        processed_size = normalized_image.size

    return PreprocessedImage(
        original_path=image_path,
        processed_path=processed_path,
        method=PREPROCESSING_METHOD,
        crop_ratio=crop_ratio,
        original_size=original_size,
        processed_size=processed_size,
    )


def center_crop(image: Image.Image, crop_ratio: float) -> Image.Image:
    width, height = image.size

    crop_width = max(int(width * crop_ratio), 1)
    crop_height = max(int(height * crop_ratio), 1)

    left = max((width - crop_width) // 2, 0)
    top = max((height - crop_height) // 2, 0)
    right = min(left + crop_width, width)
    bottom = min(top + crop_height, height)

    if right <= left:
        right = min(left + 1, width)

    if bottom <= top:
        bottom = min(top + 1, height)

    return image.crop((left, top, right, bottom))


def build_processed_path(image_path: Path) -> Path:
    safe_stem = image_path.stem.replace(" ", "_")
    return RUNTIME_SCAN_DIR / f"{safe_stem}_processed.jpg"