from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


SAMPLE_TABLE = "comparator_samples"
IMAGE_TABLE = "comparator_images"


def build_headers(service_role_key: str) -> dict[str, str]:
    headers = {
        "apikey": service_role_key,
        "Content-Type": "application/json",
    }

    if service_role_key.startswith("eyJ"):
        headers["Authorization"] = f"Bearer {service_role_key}"

    return headers


def request_json(
    endpoint: str,
    method: str,
    service_role_key: str,
) -> Any:
    request = Request(
        endpoint,
        method=method,
        headers=build_headers(service_role_key),
    )

    try:
        with urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Supabase HTTP error {error.code}: {error_body}") from error
    except URLError as error:
        raise RuntimeError(f"Supabase connection error: {error}") from error


def fetch_sample_by_code(
    supabase_url: str,
    service_role_key: str,
    code: str,
) -> dict[str, Any] | None:
    encoded_code = quote(code, safe="")
    endpoint = (
        f"{supabase_url}/rest/v1/{SAMPLE_TABLE}"
        f"?select=*&code=eq.{encoded_code}&limit=1"
    )

    rows = request_json(
        endpoint=endpoint,
        method="GET",
        service_role_key=service_role_key,
    )

    if not rows:
        return None

    return rows[0]


def fetch_images_by_sample_id(
    supabase_url: str,
    service_role_key: str,
    sample_id: str,
) -> list[dict[str, Any]]:
    endpoint = (
        f"{supabase_url}/rest/v1/{IMAGE_TABLE}"
        f"?select=*&sample_id=eq.{sample_id}&order=image_type.asc"
    )

    rows = request_json(
        endpoint=endpoint,
        method="GET",
        service_role_key=service_role_key,
    )

    return rows or []


def build_result_payload(
    sample: dict[str, Any],
    images: list[dict[str, Any]],
) -> dict[str, Any]:
    raw_image = next(
        (image for image in images if image.get("image_type") == "raw"),
        None,
    )
    scale_image = next(
        (image for image in images if image.get("image_type") == "scale"),
        None,
    )

    return {
        "match_type": "comparator_similarity",
        "message": (
            f"This scanned material is visually similar to comparator sample "
            f"{sample.get('code')}."
        ),
        "matched_sample": {
            "id": sample.get("id"),
            "code": sample.get("code"),
            "zone": sample.get("zone"),
            "color": sample.get("color"),
            "size_text": sample.get("size_text"),
            "composition": sample.get("composition"),
            "description": sample.get("description"),
        },
        "qaqc": {
            "ni": sample.get("ni"),
            "co": sample.get("co"),
            "fe": sample.get("fe"),
            "sio2": sample.get("sio2"),
            "cao": sample.get("cao"),
            "mgo": sample.get("mgo"),
            "fe_ni": sample.get("fe_ni"),
            "s_m": sample.get("s_m"),
        },
        "images": {
            "raw": {
                "storage_path": raw_image.get("storage_path") if raw_image else None,
                "local_path": raw_image.get("local_path") if raw_image else None,
            },
            "scale": {
                "storage_path": scale_image.get("storage_path") if scale_image else None,
                "local_path": scale_image.get("local_path") if scale_image else None,
            },
        },
        "similarity": {
            "score": None,
            "confidence_label": "placeholder",
            "note": "AI similarity calculation will be added in the AI pipeline sprint.",
        },
    }