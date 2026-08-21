from __future__ import annotations

from collections import defaultdict
from typing import Any


ZONE_SELECTION_METHOD = "zone_level_selection_v1"

ZONE_SOFT_PRIOR = {
    "earthy saprolite": 0.040,
    "rocky saprolite": 0.040,
    "weathering rock": 0.020,
    "red limonite": 0.015,
    "yellow limonite": 0.015,
    "fresh rock": -0.045,
    "top soil": -0.010,
    "clay": -0.015,
    "coal": -0.030,
    "silica boxwork": -0.020,
}

FRESH_ROCK_CLOSE_MARGIN = 0.045


def select_zone_level_candidate(
    ranked_candidates: list[dict[str, Any]],
    candidate_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    sample_by_code = {
        sample.get("code"): sample
        for sample in candidate_rows
        if sample.get("code")
    }

    enriched_candidates = []

    for rank, candidate in enumerate(ranked_candidates, start=1):
        code = candidate.get("code")
        sample = sample_by_code.get(code)

        if not sample:
            continue

        visual_score = to_float(candidate.get("score"))
        zone = normalize_zone(sample.get("zone"))

        enriched_candidates.append(
            {
                **candidate,
                "rank": rank,
                "visual_score": visual_score,
                "zone": sample.get("zone"),
                "normalized_zone": zone,
            }
        )

    if not enriched_candidates:
        return {
            "code": ranked_candidates[0].get("code") if ranked_candidates else None,
            "score": ranked_candidates[0].get("score") if ranked_candidates else None,
            "selection_method": ZONE_SELECTION_METHOD,
            "selection_reason": "fallback_no_candidate_rows",
            "zone_scores": [],
        }

    zone_scores = calculate_zone_scores(enriched_candidates)
    selected_zone = choose_selected_zone(zone_scores)

    zone_candidates = [
        candidate
        for candidate in enriched_candidates
        if candidate["normalized_zone"] == selected_zone
    ]

    if not zone_candidates:
        zone_candidates = enriched_candidates

    selected_candidate = sorted(
        zone_candidates,
        key=lambda item: item["visual_score"],
        reverse=True,
    )[0]

    selected_candidate = dict(selected_candidate)
    selected_candidate.update(
        {
            "score": selected_candidate["visual_score"],
            "selection_method": ZONE_SELECTION_METHOD,
            "selected_zone": selected_zone,
            "selection_reason": "zone_level_distribution",
            "zone_scores": zone_scores,
        }
    )

    return selected_candidate


def calculate_zone_scores(
    enriched_candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for candidate in enriched_candidates:
        grouped[candidate["normalized_zone"]].append(candidate)

    total_candidates = len(enriched_candidates)
    zone_scores: list[dict[str, Any]] = []

    for zone, candidates in grouped.items():
        candidates_sorted = sorted(
            candidates,
            key=lambda item: item["visual_score"],
            reverse=True,
        )

        best_score = candidates_sorted[0]["visual_score"]
        top_scores = [candidate["visual_score"] for candidate in candidates_sorted[:3]]
        average_top_score = sum(top_scores) / len(top_scores)

        frequency_score = len(candidates_sorted) / total_candidates
        rank_bonus = calculate_rank_bonus(candidates_sorted)
        soft_prior = ZONE_SOFT_PRIOR.get(zone, 0.0)

        zone_score = (
            best_score * 0.45
            + average_top_score * 0.30
            + frequency_score * 0.15
            + rank_bonus * 0.10
            + soft_prior
        )

        zone_scores.append(
            {
                "zone": candidates_sorted[0]["zone"],
                "normalized_zone": zone,
                "zone_score": round(zone_score, 4),
                "best_score": round(best_score, 4),
                "average_top_score": round(average_top_score, 4),
                "frequency_score": round(frequency_score, 4),
                "rank_bonus": round(rank_bonus, 4),
                "soft_prior": round(soft_prior, 4),
                "count": len(candidates_sorted),
                "best_code": candidates_sorted[0].get("code"),
            }
        )

    return sorted(
        zone_scores,
        key=lambda item: item["zone_score"],
        reverse=True,
    )


def choose_selected_zone(zone_scores: list[dict[str, Any]]) -> str:
    if not zone_scores:
        return ""

    best_zone = zone_scores[0]["normalized_zone"]

    if best_zone != "fresh rock":
        return best_zone

    for candidate_zone in zone_scores[1:]:
        normalized_zone = candidate_zone["normalized_zone"]

        if normalized_zone not in {
            "rocky saprolite",
            "earthy saprolite",
            "weathering rock",
        }:
            continue

        score_gap = zone_scores[0]["zone_score"] - candidate_zone["zone_score"]

        if score_gap <= FRESH_ROCK_CLOSE_MARGIN:
            return normalized_zone

    return best_zone


def calculate_rank_bonus(candidates: list[dict[str, Any]]) -> float:
    bonus = 0.0

    for candidate in candidates:
        rank = int(candidate.get("rank") or 99)

        if rank <= 3:
            bonus += 0.45
        elif rank <= 10:
            bonus += 0.25
        elif rank <= 25:
            bonus += 0.10

    return min(bonus, 1.0)


def normalize_zone(value: Any) -> str:
    if value is None:
        return ""

    return str(value).strip().lower().replace("_", " ")


def to_float(value: Any) -> float:
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return 0.0

    return max(0.0, min(parsed, 1.0))