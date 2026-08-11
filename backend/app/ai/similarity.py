from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


DEFAULT_COMPARATOR_CODE = "BG1 - 01"


@dataclass(frozen=True)
class SimilarityCandidate:
    code: str
    score: float | None
    confidence_label: str
    method: str
    note: str


def find_best_candidate(scan_image_path: Path) -> SimilarityCandidate:
    """
    Temporary AI similarity interface.

    Sprint 08A only prepares the backend contract.
    Real image similarity will be implemented later using image features,
    then OpenCV/OpenCLIP embeddings.

    The API should call this function instead of hardcoding the comparator code.
    """
    if not scan_image_path.exists():
        raise FileNotFoundError(f"Scan image not found: {scan_image_path}")

    return SimilarityCandidate(
        code=DEFAULT_COMPARATOR_CODE,
        score=None,
        confidence_label="placeholder",
        method="pre_ai_placeholder",
        note=(
            "AI similarity pipeline is prepared, but real visual matching "
            "has not been implemented yet."
        ),
    )