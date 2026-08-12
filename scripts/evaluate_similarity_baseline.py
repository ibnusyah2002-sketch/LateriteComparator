from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
BACKEND_DIR = REPO_ROOT / "backend"
SAMPLES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_samples_preview.json"
OUTPUT_DIR = REPO_ROOT / "backend" / "data_preview"
OUTPUT_PATH = OUTPUT_DIR / "similarity_evaluation_report.json"

sys.path.insert(0, str(BACKEND_DIR))

from app.ai.similarity import find_best_candidate, load_feature_cache  # noqa: E402


def main() -> int:
    args = parse_args()

    feature_cache = load_feature_cache()
    sample_rows = load_json(SAMPLES_PREVIEW_PATH)
    sample_by_code = {
        sample.get("code"): sample
        for sample in sample_rows
        if sample.get("code")
    }

    if not feature_cache:
        print("Feature cache is empty. Run scripts/build_image_feature_cache.py first.")
        return 1

    selected_features = feature_cache

    if args.limit:
        selected_features = selected_features[: args.limit]

    print("LCGC Similarity Baseline Evaluation")
    print("=" * 42)
    print(f"Feature cache count: {len(feature_cache)}")
    print(f"Samples metadata count: {len(sample_by_code)}")
    print(f"Evaluation count: {len(selected_features)}")
    print("")

    results: list[dict[str, Any]] = []
    warnings: list[str] = []

    for index, feature in enumerate(selected_features, start=1):
        input_code = feature.get("code")
        local_path_text = feature.get("local_path")

        if not input_code or not local_path_text:
            warnings.append(f"Row {index}: missing code or local_path.")
            continue

        image_path = REPO_ROOT / local_path_text

        if not image_path.exists():
            warnings.append(f"{input_code}: image not found at {local_path_text}.")
            continue

        input_sample = sample_by_code.get(input_code, {})
        input_zone = input_sample.get("zone")

        try:
            similarity_result = find_best_candidate(image_path)
        except Exception as error:
            warnings.append(f"{input_code}: similarity failed: {error}")
            continue

        top_candidates = build_candidate_payloads(
            ranked_candidates=similarity_result.ranked_candidates,
            sample_by_code=sample_by_code,
        )

        top_codes = [
            candidate.get("code")
            for candidate in top_candidates
            if candidate.get("code")
        ]

        top_zones = [
            candidate.get("zone")
            for candidate in top_candidates
            if candidate.get("zone")
        ]

        top_1 = top_candidates[0] if top_candidates else {}

        result = {
            "input_code": input_code,
            "input_zone": input_zone,
            "input_color": input_sample.get("color"),
            "top_1_code": top_1.get("code"),
            "top_1_zone": top_1.get("zone"),
            "top_1_score": top_1.get("score"),
            "exact_top_1": input_code == top_1.get("code"),
            "exact_in_top_3": input_code in top_codes[:3],
            "exact_in_top_5": input_code in top_codes[:5],
            "zone_top_1": bool(input_zone and input_zone == top_1.get("zone")),
            "zone_in_top_3": bool(input_zone and input_zone in top_zones[:3]),
            "zone_in_top_5": bool(input_zone and input_zone in top_zones[:5]),
            "top_candidates": top_candidates,
        }

        results.append(result)

        if index % 25 == 0 or index == len(selected_features):
            print(f"Evaluated: {index}/{len(selected_features)}")

    summary = build_summary(results)

    payload = {
        "generated_at": datetime.now().isoformat(),
        "method": "color_feature_v1",
        "description": (
            "Self-test evaluation using comparator raw images as input. "
            "This checks whether each known comparator image can retrieve itself "
            "or similar candidates from the local feature cache."
        ),
        "total_feature_cache": len(feature_cache),
        "total_samples_metadata": len(sample_by_code),
        "total_evaluated": len(results),
        "summary": summary,
        "zone_summary": build_zone_summary(results),
        "warnings": warnings,
        "results": results,
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print("")
    print_summary(summary)
    print("")
    print(f"Warnings: {len(warnings)}")
    print(f"Output: {to_repo_path(OUTPUT_PATH)}")

    if warnings:
        print("\nWarnings preview:")
        for warning in warnings[:20]:
            print(f"- {warning}")

    print("\nStatus: PASS")
    return 0


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
    total = len(results)

    if total == 0:
        return {
            "total": 0,
            "exact_top_1_rate": 0,
            "exact_top_3_rate": 0,
            "exact_top_5_rate": 0,
            "zone_top_1_rate": 0,
            "zone_top_3_rate": 0,
            "zone_top_5_rate": 0,
        }

    exact_top_1 = count_true(results, "exact_top_1")
    exact_top_3 = count_true(results, "exact_in_top_3")
    exact_top_5 = count_true(results, "exact_in_top_5")
    zone_top_1 = count_true(results, "zone_top_1")
    zone_top_3 = count_true(results, "zone_in_top_3")
    zone_top_5 = count_true(results, "zone_in_top_5")

    return {
        "total": total,
        "exact_top_1_count": exact_top_1,
        "exact_top_1_rate": rate(exact_top_1, total),
        "exact_top_3_count": exact_top_3,
        "exact_top_3_rate": rate(exact_top_3, total),
        "exact_top_5_count": exact_top_5,
        "exact_top_5_rate": rate(exact_top_5, total),
        "zone_top_1_count": zone_top_1,
        "zone_top_1_rate": rate(zone_top_1, total),
        "zone_top_3_count": zone_top_3,
        "zone_top_3_rate": rate(zone_top_3, total),
        "zone_top_5_count": zone_top_5,
        "zone_top_5_rate": rate(zone_top_5, total),
    }


def build_zone_summary(results: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for result in results:
        zone = result.get("input_zone") or "Unknown"
        grouped[zone].append(result)

    zone_summary: dict[str, Any] = {}

    for zone, zone_results in sorted(grouped.items()):
        zone_summary[zone] = build_summary(zone_results)

    return zone_summary


def count_true(results: list[dict[str, Any]], key: str) -> int:
    return sum(1 for result in results if result.get(key) is True)


def rate(count: int, total: int) -> float:
    if total == 0:
        return 0

    return round(count / total, 4)


def print_summary(summary: dict[str, Any]) -> None:
    print("Summary")
    print("-" * 20)
    print(f"Total evaluated       : {summary['total']}")
    print(
        f"Exact top-1 match     : {summary.get('exact_top_1_count', 0)} "
        f"({summary['exact_top_1_rate'] * 100:.2f}%)"
    )
    print(
        f"Exact in top-3        : {summary.get('exact_top_3_count', 0)} "
        f"({summary['exact_top_3_rate'] * 100:.2f}%)"
    )
    print(
        f"Exact in top-5        : {summary.get('exact_top_5_count', 0)} "
        f"({summary['exact_top_5_rate'] * 100:.2f}%)"
    )
    print(
        f"Zone top-1 match      : {summary.get('zone_top_1_count', 0)} "
        f"({summary['zone_top_1_rate'] * 100:.2f}%)"
    )
    print(
        f"Zone in top-3         : {summary.get('zone_top_3_count', 0)} "
        f"({summary['zone_top_3_rate'] * 100:.2f}%)"
    )
    print(
        f"Zone in top-5         : {summary.get('zone_top_5_count', 0)} "
        f"({summary['zone_top_5_rate'] * 100:.2f}%)"
    )


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
        description="Evaluate LCGC color_feature_v1 baseline using comparator raw images."
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit number of comparator images to evaluate.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())