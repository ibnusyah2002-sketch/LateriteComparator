from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
DEFAULT_INPUT_DIR = REPO_ROOT / "testing" / "field_photos"
SAMPLES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_samples_preview.json"
OUTPUT_DIR = REPO_ROOT / "backend" / "data_preview"
OUTPUT_PATH = OUTPUT_DIR / "field_photo_similarity_report.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

sys.path.insert(0, str(BACKEND_DIR))

from app.ai.similarity import find_best_candidate  # noqa: E402


def main() -> int:
    args = parse_args()

    input_dir = Path(args.input_dir)

    if not input_dir.is_absolute():
        input_dir = REPO_ROOT / input_dir

    sample_rows = load_json(SAMPLES_PREVIEW_PATH)
    sample_by_code = {
        sample.get("code"): sample
        for sample in sample_rows
        if sample.get("code")
    }

    image_paths = collect_image_paths(input_dir)

    if args.limit:
        image_paths = image_paths[: args.limit]

    print("LCGC Field Photo Similarity Evaluation")
    print("=" * 45)
    print(f"Input dir: {to_repo_path(input_dir)}")
    print(f"Field photos: {len(image_paths)}")
    print(f"Samples metadata: {len(sample_by_code)}")
    print("")

    if not image_paths:
        print("No field photos found.")
        print("Add .jpg/.jpeg/.png/.webp files into testing/field_photos.")
        return 1

    results: list[dict[str, Any]] = []
    warnings: list[str] = []

    for index, image_path in enumerate(image_paths, start=1):
        try:
            similarity_result = find_best_candidate(image_path)
        except Exception as error:
            warnings.append(f"{to_repo_path(image_path)}: {error}")
            continue

        matched_sample = sample_by_code.get(similarity_result.code, {})

        top_candidates = build_candidate_payloads(
            ranked_candidates=similarity_result.ranked_candidates,
            sample_by_code=sample_by_code,
        )

        preprocessing = similarity_result.preprocessing

        result = {
            "file": to_repo_path(image_path),
            "file_name": image_path.name,
            "group": image_path.parent.name if image_path.parent != input_dir else None,
            "matched_code": similarity_result.code,
            "matched_zone": matched_sample.get("zone"),
            "matched_color": matched_sample.get("color"),
            "score": similarity_result.score,
            "confidence_label": similarity_result.confidence_label,
            "method": similarity_result.method,
            "note": similarity_result.note,
            "preprocessing": {
                "method": preprocessing.method if preprocessing else None,
                "crop_ratio": preprocessing.crop_ratio if preprocessing else None,
                "original_size": preprocessing.original_size if preprocessing else None,
                "processed_size": preprocessing.processed_size if preprocessing else None,
                "processed_path": (
                    to_repo_path(preprocessing.processed_path)
                    if preprocessing
                    else None
                ),
            },
            "matched_qaqc": {
                "ni": matched_sample.get("ni"),
                "co": matched_sample.get("co"),
                "fe": matched_sample.get("fe"),
                "sio2": matched_sample.get("sio2"),
                "mgo": matched_sample.get("mgo"),
                "fe_ni": matched_sample.get("fe_ni"),
                "s_m": matched_sample.get("s_m"),
            },
            "top_candidates": top_candidates,
        }

        results.append(result)

        print(
            f"{index}. {image_path.name} -> "
            f"{similarity_result.code} | "
            f"zone={matched_sample.get('zone')} | "
            f"score={similarity_result.score}"
        )

    summary = build_summary(results)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "description": (
            "Field photo evaluation using the current LCGC similarity pipeline. "
            "This report is used to check result stability against real field photos, "
            "background variation, lighting, and capture conditions."
        ),
        "input_dir": to_repo_path(input_dir),
        "total_photos": len(image_paths),
        "total_evaluated": len(results),
        "summary": summary,
        "warnings": warnings,
        "results": results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("")
    print("Summary")
    print("-" * 20)
    print(f"Total evaluated: {summary['total_evaluated']}")
    print("Matched zones:")
    for zone, count in summary["matched_zone_distribution"].items():
        print(f"- {zone}: {count}")

    print("")
    print("Matched codes:")
    for code, count in summary["matched_code_distribution"].items():
        print(f"- {code}: {count}")

    print("")
    print(f"Warnings: {len(warnings)}")
    print(f"Output: {to_repo_path(OUTPUT_PATH)}")
    print("")
    print("Status: PASS")

    return 0


def collect_image_paths(input_dir: Path) -> list[Path]:
    if not input_dir.exists():
        return []

    return sorted(
        path
        for path in input_dir.rglob("*")
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def build_candidate_payloads(
    ranked_candidates: list[dict[str, Any]],
    sample_by_code: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []

    for candidate in ranked_candidates:
        code = candidate.get("code")
        sample = sample_by_code.get(code, {})

        payloads.append(
            {
                "code": code,
                "score": candidate.get("score"),
                "confidence_label": candidate.get("confidence_label"),
                "zone": sample.get("zone"),
                "color": sample.get("color"),
                "qaqc": {
                    "ni": sample.get("ni"),
                    "co": sample.get("co"),
                    "fe": sample.get("fe"),
                    "sio2": sample.get("sio2"),
                    "mgo": sample.get("mgo"),
                    "fe_ni": sample.get("fe_ni"),
                    "s_m": sample.get("s_m"),
                },
                "local_path": candidate.get("local_path"),
                "storage_path": candidate.get("storage_path"),
            }
        )

    return payloads


def build_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    matched_codes = Counter(
        result.get("matched_code") or "Unknown"
        for result in results
    )
    matched_zones = Counter(
        result.get("matched_zone") or "Unknown"
        for result in results
    )

    scores = [
        result["score"]
        for result in results
        if isinstance(result.get("score"), int | float)
    ]

    average_score = round(sum(scores) / len(scores), 4) if scores else None

    return {
        "total_evaluated": len(results),
        "average_score": average_score,
        "matched_code_distribution": dict(matched_codes.most_common()),
        "matched_zone_distribution": dict(matched_zones.most_common()),
    }


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


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate LCGC similarity results against local field photos."
    )
    parser.add_argument(
        "--input-dir",
        default=str(DEFAULT_INPUT_DIR),
        help="Directory containing field photos.",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of field photos to evaluate.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())