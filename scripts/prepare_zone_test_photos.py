from __future__ import annotations

import argparse
import json
import random
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
SAMPLES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_samples_preview.json"
IMAGES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_images_preview.json"
OUTPUT_DIR = REPO_ROOT / "testing" / "field_photos"

DEFAULT_PHOTOS_PER_ZONE = 5
DEFAULT_RANDOM_SEED = 21


def main() -> int:
    args = parse_args()
    photos_per_zone = args.photos_per_zone
    random_seed = args.seed

    random.seed(random_seed)

    samples = load_json(SAMPLES_PREVIEW_PATH)
    images = load_json(IMAGES_PREVIEW_PATH)

    sample_by_code = {
        sample.get("code"): sample
        for sample in samples
        if sample.get("code")
    }

    raw_images_by_code: dict[str, dict[str, Any]] = {}

    for image in images:
        code = image.get("code")
        image_type = image.get("image_type")
        local_path = image.get("local_path")

        if not code or image_type != "raw" or not local_path:
            continue

        path = REPO_ROOT / local_path

        if path.exists():
            raw_images_by_code[code] = image

    grouped_by_zone: dict[str, list[str]] = defaultdict(list)

    for code, sample in sample_by_code.items():
        zone = sample.get("zone") or "Unknown"

        if code not in raw_images_by_code:
            continue

        grouped_by_zone[zone].append(code)

    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    manifest: list[dict[str, Any]] = []

    print("LCGC Database Zone Photo Preparation")
    print("=" * 45)
    print(f"Samples: {len(samples)}")
    print(f"Raw images available: {len(raw_images_by_code)}")
    print(f"Photos per zone: {photos_per_zone}")
    print(f"Random seed: {random_seed}")
    print(f"Selection strategy: randomized front-balanced")
    print(f"Output: {to_repo_path(OUTPUT_DIR)}")
    print("")

    for zone in sorted(grouped_by_zone):
        selected_codes = select_front_balanced_random_codes(
            codes=grouped_by_zone[zone],
            sample_by_code=sample_by_code,
            limit=photos_per_zone,
        )

        zone_dir = OUTPUT_DIR / slugify(zone)
        zone_dir.mkdir(parents=True, exist_ok=True)

        print(f"{zone}: {len(selected_codes)} photo(s)")

        for index, code in enumerate(selected_codes, start=1):
            image = raw_images_by_code[code]
            source_path = REPO_ROOT / image["local_path"]

            extension = source_path.suffix.lower() or ".jpg"
            sample = sample_by_code.get(code, {})
            front = get_front(sample, code)

            destination_name = (
                f"{index:02d}_{safe_filename(front)}_{safe_filename(code)}_raw{extension}"
            )
            destination_path = zone_dir / destination_name

            shutil.copy2(source_path, destination_path)

            manifest.append(
                {
                    "expected_zone": zone,
                    "front": front,
                    "code": code,
                    "source_path": to_repo_path(source_path),
                    "copied_path": to_repo_path(destination_path),
                    "ni": sample.get("ni"),
                    "fe": sample.get("fe"),
                    "mgo": sample.get("mgo"),
                    "sio2": sample.get("sio2"),
                    "color": sample.get("color"),
                }
            )

            print(f"  - {code} | front={front} -> {to_repo_path(destination_path)}")

        print("")

    manifest_path = OUTPUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Manifest: {to_repo_path(manifest_path)}")
    print("Status: PASS")

    return 0


def select_front_balanced_random_codes(
    codes: list[str],
    sample_by_code: dict[str, dict[str, Any]],
    limit: int,
) -> list[str]:
    grouped_by_front: dict[str, list[str]] = defaultdict(list)

    for code in codes:
        sample = sample_by_code.get(code, {})
        front = get_front(sample, code)
        grouped_by_front[front].append(code)

    for front_codes in grouped_by_front.values():
        random.shuffle(front_codes)

    fronts = list(grouped_by_front.keys())
    random.shuffle(fronts)

    selected: list[str] = []

    while len(selected) < limit and fronts:
        next_fronts: list[str] = []

        for front in fronts:
            if len(selected) >= limit:
                break

            front_codes = grouped_by_front[front]

            if not front_codes:
                continue

            selected.append(front_codes.pop(0))

            if front_codes:
                next_fronts.append(front)

        fronts = next_fronts
        random.shuffle(fronts)

    if len(selected) < limit:
        remaining_codes = [
            code
            for code in codes
            if code not in selected
        ]

        random.shuffle(remaining_codes)
        selected.extend(remaining_codes[: limit - len(selected)])

    return selected[:limit]


def get_front(sample: dict[str, Any], code: str) -> str:
    front = (
        sample.get("front")
        or sample.get("Front")
        or sample.get("pit")
        or sample.get("Pit")
    )

    if front:
        return str(front).strip()

    return infer_front_from_code(code)


def infer_front_from_code(code: str) -> str:
    if not code:
        return "Unknown"

    if "-" in code:
        return code.split("-", maxsplit=1)[0].strip()

    return code.split()[0].strip()


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {to_repo_path(path)}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected list JSON: {to_repo_path(path)}")

    return data


def slugify(value: str) -> str:
    return (
        value.strip()
        .lower()
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace("-", "_")
    )


def safe_filename(value: str) -> str:
    return (
        value.strip()
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
    )


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Prepare randomized and front-balanced database zone photos for LCGC testing."
    )
    parser.add_argument(
        "--photos-per-zone",
        type=int,
        default=DEFAULT_PHOTOS_PER_ZONE,
        help="Number of raw comparator photos to copy per zone.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=DEFAULT_RANDOM_SEED,
        help="Random seed for reproducible sampling.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())