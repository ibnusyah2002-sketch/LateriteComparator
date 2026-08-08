from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_ROOT / "backend" / ".env.local"

SAMPLE_TABLE = "comparator_samples"
IMAGE_TABLE = "comparator_images"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Test Supabase read access for LCGC comparator data."
    )
    parser.add_argument(
        "--code",
        default="BG1 - 01",
        help="Comparator sample code to fetch.",
    )
    args = parser.parse_args()

    env = load_env_file(ENV_PATH)

    supabase_url = required_env(env, "SUPABASE_URL").rstrip("/")
    service_role_key = required_env(env, "SUPABASE_SERVICE_ROLE_KEY")

    sample = fetch_sample_by_code(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
        code=args.code,
    )

    if sample is None:
        print(f"Sample not found: {args.code}")
        return 1

    images = fetch_images_by_sample_id(
        supabase_url=supabase_url,
        service_role_key=service_role_key,
        sample_id=sample["id"],
    )

    result_payload = build_result_payload(sample, images)

    print("LCGC Supabase Read Test")
    print("=" * 28)
    print(f"Sample code: {sample['code']}")
    print(f"Sample ID: {sample['id']}")
    print(f"Images found: {len(images)}")
    print("")
    print("Result payload preview:")
    print(json.dumps(result_payload, ensure_ascii=False, indent=2))

    if len(images) < 2:
        print("\nStatus: REVIEW REQUIRED")
        print("Sample was found, but image rows are incomplete.")
        return 1

    print("\nStatus: PASS")
    print("Supabase sample and image read test succeeded.")
    return 0


def load_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        raise FileNotFoundError(f"Env file not found: {to_repo_path(path)}")

    env: dict[str, str] = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        clean_line = line.strip()

        if not clean_line or clean_line.startswith("#"):
            continue

        if "=" not in clean_line:
            continue

        key, value = clean_line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")

    return env


def required_env(env: dict[str, str], key: str) -> str:
    value = env.get(key) or os.environ.get(key)

    if not value:
        raise ValueError(f"Missing required env value: {key}")

    return value


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
            "note": "Similarity calculation will be added in the AI pipeline sprint.",
        },
    }


def request_json(
    endpoint: str,
    method: str,
    service_role_key: str,
) -> Any:
    request = Request(
        endpoint,
        method=method,
        headers={
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=120) as response:
            body = response.read().decode("utf-8")
            return json.loads(body) if body else None
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase HTTP error {error.code}: {error_body}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Supabase connection error: {error}") from error


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"\nRead test failed: {error}", file=sys.stderr)
        raise SystemExit(1)