from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from PIL import Image, ImageStat


FEATURE_VERSION = "color_feature_v1"
HISTOGRAM_BINS_PER_CHANNEL = 3
HISTOGRAM_VECTOR_LENGTH = HISTOGRAM_BINS_PER_CHANNEL ** 3


def extract_image_feature(image_path: Path) -> dict[str, Any]:
    if not image_path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(image_path) as image:
        rgb_image = image.convert("RGB")
        rgb_image.thumbnail((160, 160))

        rgb_stat = ImageStat.Stat(rgb_image)
        mean_rgb = [value / 255 for value in rgb_stat.mean]
        std_rgb = [value / 255 for value in rgb_stat.stddev]

        hsv_image = rgb_image.convert("HSV")
        hsv_stat = ImageStat.Stat(hsv_image)
        saturation = hsv_stat.mean[1] / 255
        brightness = hsv_stat.mean[2] / 255

        histogram = build_rgb_histogram(rgb_image)

    vector = [
        *mean_rgb,
        *std_rgb,
        saturation,
        brightness,
        *histogram,
    ]

    return {
        "version": FEATURE_VERSION,
        "vector": vector,
        "summary": {
            "mean_rgb": mean_rgb,
            "std_rgb": std_rgb,
            "saturation": saturation,
            "brightness": brightness,
            "histogram_bins": HISTOGRAM_VECTOR_LENGTH,
        },
    }


def build_rgb_histogram(image: Image.Image) -> list[float]:
    small_image = image.resize((64, 64))
    pixels = list(small_image.getdata())

    histogram = [0 for _ in range(HISTOGRAM_VECTOR_LENGTH)]

    for red, green, blue in pixels:
        red_bin = min(red // 86, 2)
        green_bin = min(green // 86, 2)
        blue_bin = min(blue // 86, 2)

        index = (
            red_bin * HISTOGRAM_BINS_PER_CHANNEL * HISTOGRAM_BINS_PER_CHANNEL
            + green_bin * HISTOGRAM_BINS_PER_CHANNEL
            + blue_bin
        )
        histogram[index] += 1

    total_pixels = len(pixels)

    if total_pixels == 0:
        return [0.0 for _ in histogram]

    return [count / total_pixels for count in histogram]


def calculate_similarity_score(
    scan_vector: list[float],
    comparator_vector: list[float],
) -> float:
    if len(scan_vector) != len(comparator_vector):
        raise ValueError("Feature vectors must have the same length.")

    squared_distance = sum(
        (scan_value - comparator_value) ** 2
        for scan_value, comparator_value in zip(scan_vector, comparator_vector)
    )

    distance = math.sqrt(squared_distance / len(scan_vector))
    score = max(0.0, 1.0 - distance)

    return round(score, 4)


def confidence_label_from_score(score: float | None) -> str:
    if score is None:
        return "placeholder"

    if score >= 0.92:
        return "high"

    if score >= 0.86:
        return "medium"

    return "low"