from __future__ import annotations

import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = REPO_ROOT / "backend"

if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.ai.similarity import find_best_candidate


MANIFEST_PATH = REPO_ROOT / "testing" / "field_photos" / "manifest.json"
SAMPLES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_samples_preview.json"
OUTPUT_PATH = REPO_ROOT / "backend" / "data_preview" / "database_zone_evaluation_report.json"


def main() -> int:
    manifest = load_json(MANIFEST_PATH)
    samples = load_json(SAMPLES_PREVIEW_PATH)

    sample_by_code = {
        sample.get("code"): sample
        for sample in samples
        if sample.get("code")
    }

    results: list[dict[str, Any]] = []

    for item in manifest:
        image_path = REPO_ROOT / item["copied_path"]
        expected_code = item["code"]
        expected_zone = item["expected_zone"]
        expected_front = item.get("front")

        candidate = find_best_candidate(image_path)
        matched_code = candidate.code
        matched_sample = sample_by_code.get(matched_code, {})
        matched_zone = matched_sample.get("zone")

        is_code_match = expected_code == matched_code
        is_zone_match = normalize(expected_zone) == normalize(matched_zone)

        results.append(
            {
                "file": item["copied_path"],
                "expected_code": expected_code,
                "expected_zone": expected_zone,
                "expected_front": expected_front,
                "matched_code": matched_code,
                "matched_zone": matched_zone,
                "score": candidate.score,
                "method": candidate.method,
                "is_code_match": is_code_match,
                "is_zone_match": is_zone_match,
            }
        )

    total = len(results)
    code_match_count = sum(1 for item in results if item["is_code_match"])
    zone_match_count = sum(1 for item in results if item["is_zone_match"])

    by_expected_zone: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in results:
        by_expected_zone[result["expected_zone"]].append(result)

    summary_by_zone = []

    for expected_zone, items in sorted(by_expected_zone.items()):
        zone_total = len(items)
        zone_correct = sum(1 for item in items if item["is_zone_match"])
        matched_distribution = Counter(item["matched_zone"] for item in items)

        summary_by_zone.append(
            {
                "expected_zone": expected_zone,
                "total": zone_total,
                "correct_zone": zone_correct,
                "zone_accuracy": round(zone_correct / zone_total, 4) if zone_total else 0,
                "matched_distribution": dict(matched_distribution),
            }
        )

    report = {
        "summary": {
            "total": total,
            "code_match_count": code_match_count,
            "code_match_accuracy": round(code_match_count / total, 4) if total else 0,
            "zone_match_count": zone_match_count,
            "zone_match_accuracy": round(zone_match_count / total, 4) if total else 0,
        },
        "summary_by_zone": summary_by_zone,
        "results": results,
    }

    OUTPUT_PATH.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("Database Zone Evaluation")
    print("=" * 40)
    print(f"Total evaluated: {total}")
    print(f"Code match: {code_match_count}/{total} ({report['summary']['code_match_accuracy']})")
    print(f"Zone match: {zone_match_count}/{total} ({report['summary']['zone_match_accuracy']})")
    print("")
    print("By expected zone:")
    for zone_summary in summary_by_zone:
        print("-" * 70)
        print(
            zone_summary["expected_zone"],
            "| accuracy:",
            zone_summary["zone_accuracy"],
            "| correct:",
            f"{zone_summary['correct_zone']}/{zone_summary['total']}",
        )
        print("Matched distribution:", zone_summary["matched_distribution"])

    print("")
    print(f"Output: {to_repo_path(OUTPUT_PATH)}")
    print("Status: PASS")

    return 0


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"File not found: {to_repo_path(path)}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected JSON list: {to_repo_path(path)}")

    return data


def normalize(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip().lower().replace("_", " ")


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    raise SystemExit(main())