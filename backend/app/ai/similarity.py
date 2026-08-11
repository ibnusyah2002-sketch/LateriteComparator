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
TOP_CANDIDATE_LIMIT = 5


@dataclass(frozen=True)
class SimilarityCandidate:
    code: str
    score: float | None
    confidence_label: str
    method: str
    note: str
    ranked_candidates: list[dict[str, Any]]


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
            ranked_candidates=[],
        )

    scan_feature = extract_image_feature(scan_image_path)
    scan_vector = scan_feature["vector"]

    all_candidates: list[dict[str, Any]] = []

    for comparator in cache:
        comparator_vector = comparator.get("feature_vector")

        if not isinstance(comparator_vector, list):
            continue

        score = calculate_similarity_score(scan_vector, comparator_vector)

        all_candidates.append(
            {
                "code": comparator.get("code"),
                "score": score,
                "confidence_label": confidence_label_from_score(score),
                "local_path": comparator.get("local_path"),
                "storage_path": comparator.get("storage_path"),
                "feature_version": comparator.get("feature_version"),
            }
        )

    if not all_candidates:
        return SimilarityCandidate(
            code=DEFAULT_COMPARATOR_CODE,
            score=None,
            confidence_label="placeholder",
            method="color_feature_fallback",
            note="No valid comparator feature vectors found. Falling back to default comparator.",
            ranked_candidates=[],
        )

    ranked_candidates = sorted(
        all_candidates,
        key=lambda item: item["score"] if item["score"] is not None else 0,
        reverse=True,
    )

    top_candidates = ranked_candidates[:TOP_CANDIDATE_LIMIT]
    best = top_candidates[0]
    score = best["score"]

    return SimilarityCandidate(
        code=best["code"] or DEFAULT_COMPARATOR_CODE,
        score=score,
        confidence_label=confidence_label_from_score(score),
        method="color_feature_v1",
        note=(
            "Matched using lightweight color statistics and RGB histogram. "
            "This is an early baseline before OpenCLIP visual embedding."
        ),
        ranked_candidates=top_candidates,
    )


def load_feature_cache() -> list[dict[str, Any]]:
    if not FEATURE_CACHE_PATH.exists():
        return []

    data = json.loads(FEATURE_CACHE_PATH.read_text(encoding="utf-8"))
    features = data.get("features", [])

    if not isinstance(features, list):
        return []

    return features