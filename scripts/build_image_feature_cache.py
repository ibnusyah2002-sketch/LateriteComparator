from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.ai.image_features import FEATURE_VERSION, extract_image_feature
from app.ai.preprocessing import PREPROCESSING_METHOD, preprocess_scan_image


IMAGES_PREVIEW_PATH = BACKEND_ROOT / "data_preview" / "comparator_images_preview.json"
FEATURE_CACHE_PATH = BACKEND_ROOT / "feature_cache" / "comparator_features.json"


def main() -> int:
    images = load_json(IMAGES_PREVIEW_PATH)

    raw_images = [
        image
        for image in images
        if image.get("image_type") == "raw"
        and image.get("code")
        and image.get("local_path")
    ]

    features: list[dict[str, Any]] = []
    warnings: list[str] = []

    print("LCGC Image Feature Cache Builder")
    print("=" * 45)
    print(f"Feature version: {FEATURE_VERSION}")
    print(f"Preprocessing method: {PREPROCESSING_METHOD}")
    print(f"Raw image rows: {len(raw_images)}")
    print("")

    for index, image in enumerate(raw_images, start=1):
        code = image["code"]
        local_path = image["local_path"]
        source_path = REPO_ROOT / local_path

        if not source_path.exists():
            warnings.append(f"{code}: source image not found: {local_path}")
            continue

        try:
            preprocessing = preprocess_scan_image(source_path)
            feature = extract_image_feature(preprocessing.processed_path)
        except Exception as error:
            warnings.append(f"{code}: failed to extract feature: {error}")
            continue

        features.append(
            {
                "code": code,
                "image_type": image.get("image_type"),
                "local_path": local_path,
                "storage_path": image.get("storage_path"),
                "feature_version": feature["version"],
                "feature_vector": feature["vector"],
                "feature_summary": feature["summary"],
                "preprocessing": {
                    "method": preprocessing.method,
                    "crop_ratio": preprocessing.crop_ratio,
                    "original_size": preprocessing.original_size,
                    "processed_size": preprocessing.processed_size,
                    "processed_path": to_repo_path(preprocessing.processed_path),
                },
            }
        )

        print(
            f"{index:03d}/{len(raw_images)} | {code} | "
            f"vector={len(feature['vector'])} | "
            f"preprocessed={preprocessing.method}"
        )

    cache_payload = {
        "feature_version": FEATURE_VERSION,
        "preprocessing_method": PREPROCESSING_METHOD,
        "total_features": len(features),
        "features": features,
        "warnings": warnings,
    }

    FEATURE_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    FEATURE_CACHE_PATH.write_text(
        json.dumps(cache_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("")
    print("Summary")
    print("-" * 45)
    print(f"Features generated: {len(features)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Output: {to_repo_path(FEATURE_CACHE_PATH)}")

    if warnings:
        print("")
        print("Warnings detail:")
        for warning in warnings:
            print(f"- {warning}")

    print("")
    print("Status: PASS" if not warnings else "Status: PASS_WITH_WARNINGS")

    return 0


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {to_repo_path(path)}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected JSON list: {to_repo_path(path)}")

    return data


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())