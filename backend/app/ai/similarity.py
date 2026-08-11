from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.ai.image_features import (
    calculate_similarity_score,
    confidence_label_from_score,
    extract_image_feature,
)


BACKEND_ROOT = Path(__file__).resolve().parents[2]
FEATURE_CACHE_PATH = BACKEND_ROOT / "feature_cache" / "comparator_features.json"
DEFAULT_COMPARATOR_CODE = "BG1 - 01"


@dataclass(frozen=True)
class SimilarityCandidate:
    code: str
    score: float | None
    confidence_label: str
    method: str
    note: str


def find_best_candidate(scan_image_path: Path) -> SimilarityCandidate:
    if not scan_image_path.exists():
        raise FileNotFoundError(f"Scan image not found: {scan_image_path}")

    cache = load_feature_cache()

    if not cache:
        return SimilarityCandidate(
            code=DEFAULT_COMPARATOR_CODE,
            score=None,
            confidence_label="placeholder",
            method="pre_ai_placeholder",
            note="Feature cache not found. Falling back to default comparator.",
        )

    scan_feature = extract_image_feature(scan_image_path)
    scan_vector = scan_feature["vector"]

    ranked_candidates: list[dict[str, Any]] = []

    for comparator in cache:
        comparator_vector = comparator.get("feature_vector")

        if not isinstance(comparator_vector, list):
            continue

        score = calculate_similarity_score(scan_vector, comparator_vector)

        ranked_candidates.append(
            {
                "code": comparator["code"],
                "score": score,
                "local_path": comparator.get("local_path"),
            }
        )

    if not ranked_candidates:
        return SimilarityCandidate(
            code=DEFAULT_COMPARATOR_CODE,
            score=None,
            confidence_label="placeholder",
            method="color_feature_fallback",
            note="No valid comparator feature vectors found. Falling back to default comparator.",
        )

    best = max(ranked_candidates, key=lambda item: item["score"])
    score = best["score"]

    return SimilarityCandidate(
        code=best["code"],
        score=score,
        confidence_label=confidence_label_from_score(score),
        method="color_feature_v1",
        note=(
            "Matched using lightweight color statistics and RGB histogram. "
            "This is an early approximation before OpenCLIP visual embedding."
        ),
    )


def load_feature_cache() -> list[dict[str, Any]]:
    if not FEATURE_CACHE_PATH.exists():
        return []

    data = json.loads(FEATURE_CACHE_PATH.read_text(encoding="utf-8"))
    features = data.get("features", [])

    if not isinstance(features, list):
        return []

    return features