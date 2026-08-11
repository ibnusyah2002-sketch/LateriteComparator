from __future__ import annotations

import json
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


SAMPLE_TABLE = "comparator_samples"
IMAGE_TABLE = "comparator_images"
SIGNED_URL_EXPIRES_IN_SECONDS = 3600


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
    payload: dict[str, Any] | None = None,
) -> Any:
    data = None

    if payload is not None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    request = Request(
        endpoint,
        data=data,
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


def fetch_samples_by_codes(
    supabase_url: str,
    service_role_key: str,
    codes: list[str],
) -> list[dict[str, Any]]:
    unique_codes = []

    for code in codes:
        if code and code not in unique_codes:
            unique_codes.append(code)

    if not unique_codes:
        return []

    encoded_values = ",".join(
        f'"{quote(code, safe="")}"'
        for code in unique_codes
    )

    endpoint = (
        f"{supabase_url}/rest/v1/{SAMPLE_TABLE}"
        f"?select=*&code=in.({encoded_values})"
    )

    rows = request_json(
        endpoint=endpoint,
        method="GET",
        service_role_key=service_role_key,
    )

    return rows or []


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


def attach_signed_urls_to_images(
    supabase_url: str,
    service_role_key: str,
    bucket: str,
    images: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    signed_images: list[dict[str, Any]] = []

    for image in images:
        signed_image = dict(image)
        storage_path = image.get("storage_path")

        if storage_path:
            signed_image["signed_url"] = create_signed_url(
                supabase_url=supabase_url,
                service_role_key=service_role_key,
                bucket=bucket,
                storage_path=storage_path,
                expires_in=SIGNED_URL_EXPIRES_IN_SECONDS,
            )
            signed_image["signed_url_expires_in"] = SIGNED_URL_EXPIRES_IN_SECONDS
        else:
            signed_image["signed_url"] = None
            signed_image["signed_url_expires_in"] = None

        signed_images.append(signed_image)

    return signed_images


def create_signed_url(
    supabase_url: str,
    service_role_key: str,
    bucket: str,
    storage_path: str,
    expires_in: int,
) -> str:
    object_path = to_storage_object_path(storage_path, bucket)
    encoded_object_path = quote(object_path, safe="/")

    endpoint = (
        f"{supabase_url}/storage/v1/object/sign/"
        f"{bucket}/{encoded_object_path}"
    )

    response = request_json(
        endpoint=endpoint,
        method="POST",
        service_role_key=service_role_key,
        payload={
            "expiresIn": expires_in,
        },
    )

    signed_url = response.get("signedURL") or response.get("signedUrl")

    if not signed_url:
        raise RuntimeError(f"Signed URL was not returned for: {storage_path}")

    return normalize_signed_url(supabase_url, signed_url)


def to_storage_object_path(storage_path: str, bucket: str) -> str:
    prefix = f"{bucket}/"

    if storage_path.startswith(prefix):
        return storage_path[len(prefix) :]

    return storage_path


def normalize_signed_url(supabase_url: str, signed_url: str) -> str:
    if signed_url.startswith("http://") or signed_url.startswith("https://"):
        return signed_url

    if signed_url.startswith("/storage/v1/"):
        return f"{supabase_url}{signed_url}"

    if signed_url.startswith("/object/"):
        return f"{supabase_url}/storage/v1{signed_url}"

    if signed_url.startswith("object/"):
        return f"{supabase_url}/storage/v1/{signed_url}"

    return f"{supabase_url}/storage/v1/{signed_url.lstrip('/')}"


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
                "signed_url": raw_image.get("signed_url") if raw_image else None,
                "signed_url_expires_in": (
                    raw_image.get("signed_url_expires_in") if raw_image else None
                ),
            },
            "scale": {
                "storage_path": scale_image.get("storage_path") if scale_image else None,
                "local_path": scale_image.get("local_path") if scale_image else None,
                "signed_url": scale_image.get("signed_url") if scale_image else None,
                "signed_url_expires_in": (
                    scale_image.get("signed_url_expires_in") if scale_image else None
                ),
            },
        },
        "similarity": {
            "score": None,
            "confidence_label": "placeholder",
            "method": "placeholder",
            "note": "Similarity calculation will be attached by analysis endpoint.",
        },
    }