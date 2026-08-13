from __future__ import annotations

from typing import Any


RERANKING_METHOD = "geology_rerank_v1"
FINAL_CANDIDATE_LIMIT = 5

VISUAL_WEIGHT = 0.60
ZONE_WEIGHT = 0.25
GRADE_WEIGHT = 0.15

GRADE_TOLERANCES = {
    "ni": 1.0,
    "fe": 12.0,
    "mgo": 15.0,
    "sio2": 20.0,
}


ZONE_FAMILY = {
    "top soil": "cover",
    "topsoil": "cover",
    "clay": "cover",
    "coal": "coal",
    "red limonite": "limonite",
    "yellow limonite": "limonite",
    "limonite": "limonite",
    "earthy saprolite": "saprolite",
    "rocky saprolite": "saprolite",
    "saprolite": "saprolite",
    "weathering rock": "rock",
    "fresh rock": "rock",
    "freshrock": "rock",
    "bedrock": "rock",
    "silica boxwork": "silica",
}


RELATED_FAMILY_SCORES = {
    frozenset(("saprolite", "rock")): 0.45,
    frozenset(("saprolite", "silica")): 0.45,
    frozenset(("rock", "silica")): 0.45,
    frozenset(("limonite", "cover")): 0.35,
    frozenset(("limonite", "saprolite")): 0.25,
}


def rerank_candidates(
    ranked_candidates: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
    anchor_code: str,
    limit: int = FINAL_CANDIDATE_LIMIT,
) -> list[dict[str, Any]]:
    sample_by_code = {
        sample.get("code"): sample
        for sample in candidate_rows
        if sample.get("code")
    }

    anchor_sample = sample_by_code.get(anchor_code, {})
    reranked_candidates: list[dict[str, Any]] = []

    for candidate in ranked_candidates:
        code = candidate.get("code")
        candidate_sample = sample_by_code.get(code, {})

        visual_score = to_float(candidate.get("score"))
        zone_score = calculate_zone_score(
            anchor_sample.get("zone"),
            candidate_sample.get("zone"),
        )
        grade_score = calculate_grade_consistency_score(
            anchor_sample,
            candidate_sample,
        )

        if not anchor_sample:
            final_score = visual_score
        else:
            final_score = (
                visual_score * VISUAL_WEIGHT
                + zone_score * ZONE_WEIGHT
                + grade_score * GRADE_WEIGHT
            )

        reranked_candidate = dict(candidate)
        reranked_candidate.update(
            {
                "score": round(final_score, 4),
                "final_score": round(final_score, 4),
                "visual_score": round(visual_score, 4),
                "zone_score": round(zone_score, 4),
                "grade_score": round(grade_score, 4),
                "ranking_method": RERANKING_METHOD,
                "anchor_code": anchor_code,
                "anchor_zone": anchor_sample.get("zone"),
            }
        )

        reranked_candidates.append(reranked_candidate)

    reranked_candidates = sorted(
        reranked_candidates,
        key=lambda item: item.get("final_score", 0),
        reverse=True,
    )

    return reranked_candidates[:limit]


def calculate_zone_score(
    anchor_zone: Any,
    candidate_zone: Any,
) -> float:
    anchor = normalize_zone(anchor_zone)
    candidate = normalize_zone(candidate_zone)

    if not anchor or not candidate:
        return 0.5

    if anchor == candidate:
        return 1.0

    anchor_family = ZONE_FAMILY.get(anchor)
    candidate_family = ZONE_FAMILY.get(candidate)

    if anchor_family and candidate_family and anchor_family == candidate_family:
        return 0.75

    related_score = RELATED_FAMILY_SCORES.get(
        frozenset((anchor_family, candidate_family))
    )

    if related_score is not None:
        return related_score

    return 0.1


def calculate_grade_consistency_score(
    anchor_sample: dict[str, Any],
    candidate_sample: dict[str, Any],
) -> float:
    scores: list[float] = []

    for element, tolerance in GRADE_TOLERANCES.items():
        anchor_value = to_optional_float(anchor_sample.get(element))
        candidate_value = to_optional_float(candidate_sample.get(element))

        if anchor_value is None or candidate_value is None:
            continue

        difference = abs(anchor_value - candidate_value)
        element_score = max(0.0, 1.0 - (difference / tolerance))
        scores.append(element_score)

    if not scores:
        return 0.5

    return sum(scores) / len(scores)


def normalize_zone(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip().lower().replace("_", " ")


def to_optional_float(value: Any) -> float | None:
    if value is None:
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def to_float(value: Any) -> float:
    parsed = to_optional_float(value)

    if parsed is None:
        return 0.0

    return max(0.0, min(parsed, 1.0))