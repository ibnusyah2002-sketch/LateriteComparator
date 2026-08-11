from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_APP_DIR = REPO_ROOT / "backend" / "app"
IMAGE_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_images_preview.json"
OUTPUT_DIR = REPO_ROOT / "backend" / "feature_cache"
OUTPUT_PATH = OUTPUT_DIR / "comparator_features.json"

sys.path.insert(0, str(REPO_ROOT / "backend"))

from app.ai.image_features import FEATURE_VERSION, extract_image_feature  # noqa: E402


def main() -> int:
    image_rows = load_json(IMAGE_PREVIEW_PATH)

    raw_rows = [
        row for row in image_rows
        if row.get("image_type") == "raw"
    ]

    features: list[dict[str, Any]] = []
    warnings: list[str] = []

    print("LCGC Image Feature Cache Builder")
    print("=" * 38)
    print(f"Source: {to_repo_path(IMAGE_PREVIEW_PATH)}")
    print(f"Raw image rows: {len(raw_rows)}")

    for index, row in enumerate(raw_rows, start=1):
        code = row.get("code")
        local_path_text = row.get("local_path")

        if not code or not local_path_text:
            warnings.append(f"Row {index}: missing code or local_path.")
            continue

        image_path = REPO_ROOT / local_path_text

        try:
            feature = extract_image_feature(image_path)
        except Exception as error:
            warnings.append(f"{code}: failed to extract feature: {error}")
            continue

        features.append(
            {
                "code": code,
                "image_type": row.get("image_type"),
                "local_path": local_path_text,
                "storage_path": row.get("storage_path"),
                "feature_version": feature["version"],
                "feature_vector": feature["vector"],
                "feature_summary": feature["summary"],
            }
        )

        if index % 25 == 0 or index == len(raw_rows):
            print(f"Processed raw images: {index}/{len(raw_rows)}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "feature_version": FEATURE_VERSION,
        "source": to_repo_path(IMAGE_PREVIEW_PATH),
        "total_features": len(features),
        "features": features,
        "warnings": warnings,
    }

    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("")
    print(f"Features generated: {len(features)}")
    print(f"Warnings: {len(warnings)}")
    print(f"Output: {to_repo_path(OUTPUT_PATH)}")

    if warnings:
        print("\nWarnings preview:")
        for warning in warnings[:20]:
            print(f"- {warning}")

        print("\nStatus: REVIEW REQUIRED")
        return 1

    print("\nStatus: PASS")
    return 0


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {to_repo_path(path)}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected list data in {to_repo_path(path)}")

    return data


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"\nFeature cache build failed: {error}", file=sys.stderr)
        raise SystemExit(1)