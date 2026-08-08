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
IMAGES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_images_preview.json"

IMAGE_TABLE = "comparator_images"
SAMPLE_TABLE = "comparator_samples"
BATCH_SIZE = 100

MIME_BY_SUFFIX = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Upload LCGC comparator images to Supabase Storage."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate image payload without uploading files.",
    )
    args = parser.parse_args()

    env = load_env_file(ENV_PATH)

    supabase_url = required_env(env, "SUPABASE_URL").rstrip("/")
    service_role_key = required_env(env, "SUPABASE_SERVICE_ROLE_KEY")
    bucket = required_env(env, "SUPABASE_STORAGE_BUCKET")

    image_previews = load_json(IMAGES_PREVIEW_PATH)
    sample_id_by_code = fetch_sample_id_by_code(supabase_url, service_role_key)

    image_rows, local_files, warnings = prepare_image_rows(
        image_previews=image_previews,
        sample_id_by_code=sample_id_by_code,
        bucket=bucket,
    )

    print("LCGC Supabase Image Upload")
    print("=" * 32)
    print(f"Source file: {to_repo_path(IMAGES_PREVIEW_PATH)}")
    print(f"Storage bucket: {bucket}")
    print(f"Source image rows: {len(image_previews)}")
    print(f"Sample IDs loaded: {len(sample_id_by_code)}")
    print(f"Rows prepared: {len(image_rows)}")
    print(f"Local files ready: {len(local_files)}")
    print(f"Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings preview:")
        for warning in warnings[:20]:
            print(f"- {warning}")

        if len(warnings) > 20:
            print(f"- ... {len(warnings) - 20} more warnings")

    if warnings:
        print("\nStatus: REVIEW REQUIRED")
        print("Fix warnings before uploading images.")
        return 1

    if args.dry_run:
        print("\nStatus: DRY RUN PASS")
        print("No image was uploaded and no database row was changed.")
        print("\nFirst image row preview:")
        print(json.dumps(image_rows[0], ensure_ascii=False, indent=2))
        return 0

    uploaded = 0

    for local_file in local_files:
        upload_storage_object(
            supabase_url=supabase_url,
            service_role_key=service_role_key,
            bucket=bucket,
            object_path=local_file["object_path"],
            local_path=local_file["local_path"],
        )
        uploaded += 1

        if uploaded % 25 == 0 or uploaded == len(local_files):
            print(f"Uploaded images: {uploaded}/{len(local_files)}")

    inserted = 0

    for batch in chunked(image_rows, BATCH_SIZE):
        upsert_image_rows(
            supabase_url=supabase_url,
            service_role_key=service_role_key,
            rows=batch,
        )
        inserted += len(batch)
        print(f"Upserted image rows: {inserted}/{len(image_rows)}")

    print("\nStatus: PASS")
    print(f"Uploaded {uploaded} images to Supabase Storage.")
    print(f"Upserted {inserted} rows to comparator_images.")
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


def load_json(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {to_repo_path(path)}")

    data = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(data, list):
        raise ValueError(f"Expected list data in {to_repo_path(path)}")

    return data


def fetch_sample_id_by_code(
    supabase_url: str,
    service_role_key: str,
) -> dict[str, str]:
    endpoint = f"{supabase_url}/rest/v1/{SAMPLE_TABLE}?select=id,code&limit=1000"

    response = request_json(
        endpoint=endpoint,
        method="GET",
        service_role_key=service_role_key,
    )

    sample_id_by_code: dict[str, str] = {}

    for row in response:
        code = row.get("code")
        sample_id = row.get("id")

        if code and sample_id:
            sample_id_by_code[code] = sample_id

    return sample_id_by_code


def prepare_image_rows(
    image_previews: list[dict[str, Any]],
    sample_id_by_code: dict[str, str],
    bucket: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str]]:
    image_rows: list[dict[str, Any]] = []
    local_files: list[dict[str, Any]] = []
    warnings: list[str] = []

    for index, image in enumerate(image_previews, start=1):
        code = clean_text(image.get("code"))
        image_type = clean_text(image.get("image_type"))
        local_path_text = clean_text(image.get("local_path"))
        storage_path = clean_text(image.get("storage_path"))

        if not code:
            warnings.append(f"Image row {index}: missing code.")
            continue

        sample_id = sample_id_by_code.get(code)

        if not sample_id:
            warnings.append(f"{code}: sample_id not found in comparator_samples.")
            continue

        if not image_type:
            warnings.append(f"{code}: missing image_type.")
            continue

        if not local_path_text:
            warnings.append(f"{code}: missing local_path.")
            continue

        if not storage_path:
            warnings.append(f"{code}: missing storage_path.")
            continue

        local_path = REPO_ROOT / local_path_text

        if not local_path.exists():
            warnings.append(f"{code}: local image file not found: {local_path_text}")
            continue

        if not local_path.is_file():
            warnings.append(f"{code}: local image path is not a file: {local_path_text}")
            continue

        suffix = local_path.suffix.lower()

        if suffix not in MIME_BY_SUFFIX:
            warnings.append(f"{code}: unsupported image extension: {local_path_text}")
            continue

        object_path = to_storage_object_path(storage_path, bucket)

        local_files.append(
            {
                "code": code,
                "image_type": image_type,
                "local_path": local_path,
                "object_path": object_path,
            }
        )

        image_rows.append(
            {
                "sample_id": sample_id,
                "code": code,
                "image_type": image_type,
                "local_path": local_path_text,
                "storage_path": storage_path,
                "public_url": None,
                "is_primary": bool(image.get("is_primary")),
                "metadata": {
                    "source": "local_dataset",
                    "object_path": object_path,
                },
            }
        )

    return image_rows, local_files, warnings


def to_storage_object_path(storage_path: str, bucket: str) -> str:
    prefix = f"{bucket}/"

    if storage_path.startswith(prefix):
        return storage_path[len(prefix) :]

    return storage_path


def upload_storage_object(
    supabase_url: str,
    service_role_key: str,
    bucket: str,
    object_path: str,
    local_path: Path,
) -> None:
    encoded_object_path = quote(object_path, safe="/")
    endpoint = f"{supabase_url}/storage/v1/object/{bucket}/{encoded_object_path}"
    mime_type = MIME_BY_SUFFIX[local_path.suffix.lower()]
    payload = local_path.read_bytes()

    request = Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": mime_type,
            "x-upsert": "true",
        },
    )

    try:
        with urlopen(request, timeout=120) as response:
            if response.status not in {200, 201}:
                raise RuntimeError(f"Unexpected Supabase Storage status: {response.status}")
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase Storage HTTP error {error.code}: {error_body}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Supabase Storage connection error: {error}") from error


def upsert_image_rows(
    supabase_url: str,
    service_role_key: str,
    rows: list[dict[str, Any]],
) -> None:
    endpoint = f"{supabase_url}/rest/v1/{IMAGE_TABLE}?on_conflict=storage_path"
    payload = json.dumps(rows, ensure_ascii=False).encode("utf-8")

    request = Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "apikey": service_role_key,
            "Authorization": f"Bearer {service_role_key}",
            "Content-Type": "application/json",
            "Prefer": "resolution=merge-duplicates,return=minimal",
        },
    )

    try:
        with urlopen(request, timeout=120) as response:
            if response.status not in {200, 201, 204}:
                raise RuntimeError(f"Unexpected Supabase response status: {response.status}")
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase HTTP error {error.code}: {error_body}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Supabase connection error: {error}") from error


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


def chunked(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def clean_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).replace("\u00a0", " ").strip()

    if text == "":
        return None

    return text


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"\nUpload failed: {error}", file=sys.stderr)
        raise SystemExit(1)