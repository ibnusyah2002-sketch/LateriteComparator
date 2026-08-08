from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


REPO_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = REPO_ROOT / "backend" / ".env.local"
SAMPLES_PREVIEW_PATH = REPO_ROOT / "backend" / "data_preview" / "comparator_samples_preview.json"

TABLE_NAME = "comparator_samples"
BATCH_SIZE = 100

INTEGER_FIELDS = {"source_no"}

NUMERIC_FIELDS = {
    "ni",
    "co",
    "fe",
    "sio2",
    "cao",
    "mgo",
    "cr2o3",
    "al2o3",
    "cr",
    "fe_ni",
    "s_m",
}

TEXT_FIELDS = {
    "code",
    "sample_code",
    "incr",
    "bc",
    "color",
    "zone",
    "size_text",
    "composition",
    "description",
    "documentation_raw",
    "documentation_si_gc",
    "ppt_reference",
    "front_reference",
}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Import LCGC comparator samples to Supabase."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and preview payload without sending data to Supabase.",
    )
    args = parser.parse_args()

    env = load_env_file(ENV_PATH)

    supabase_url = required_env(env, "SUPABASE_URL").rstrip("/")
    service_role_key = required_env(env, "SUPABASE_SERVICE_ROLE_KEY")

    samples = load_json(SAMPLES_PREVIEW_PATH)
    normalized_samples, warnings = normalize_samples(samples)

    print("LCGC Supabase Sample Import")
    print("=" * 34)
    print(f"Source file: {to_repo_path(SAMPLES_PREVIEW_PATH)}")
    print(f"Target table: {TABLE_NAME}")
    print(f"Rows prepared: {len(normalized_samples)}")
    print(f"Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings preview:")
        for warning in warnings[:20]:
            print(f"- {warning}")

        if len(warnings) > 20:
            print(f"- ... {len(warnings) - 20} more warnings")

    if args.dry_run:
        print("\nStatus: DRY RUN PASS")
        print("No data was sent to Supabase.")
        print("\nFirst row preview:")
        print(json.dumps(normalized_samples[0], ensure_ascii=False, indent=2))
        return 0

    total_uploaded = 0

    for batch in chunked(normalized_samples, BATCH_SIZE):
        upsert_samples(
            supabase_url=supabase_url,
            service_role_key=service_role_key,
            rows=batch,
        )
        total_uploaded += len(batch)
        print(f"Uploaded/upserted rows: {total_uploaded}/{len(normalized_samples)}")

    print("\nStatus: PASS")
    print(f"Imported/upserted {total_uploaded} sample rows to Supabase.")
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


def normalize_samples(samples: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[str]]:
    normalized_samples: list[dict[str, Any]] = []
    warnings: list[str] = []

    for index, sample in enumerate(samples, start=1):
        code = clean_text(sample.get("code"))

        if not code:
            warnings.append(f"Row {index}: skipped because code is empty.")
            continue

        normalized: dict[str, Any] = {}

        normalized["code"] = code
        normalized["sample_date"] = normalize_date(sample.get("sample_date"), code, warnings)

        for field in INTEGER_FIELDS:
            normalized[field] = normalize_integer(sample.get(field), code, field, warnings)

        for field in NUMERIC_FIELDS:
            normalized[field] = normalize_numeric(sample.get(field), code, field, warnings)

        for field in TEXT_FIELDS:
            if field == "code":
                continue

            normalized[field] = clean_text(sample.get(field))

        normalized["status"] = "active"

        normalized_samples.append(normalized)

    if not normalized_samples:
        raise ValueError("No valid sample rows found after normalization.")

    return normalized_samples, warnings


def normalize_integer(
    value: Any,
    code: str,
    field: str,
    warnings: list[str],
) -> int | None:
    text = clean_text(value)

    if text is None:
        return None

    try:
        return int(float(text.replace(",", ".")))
    except ValueError:
        warnings.append(f"{code}: {field}='{text}' could not be converted to integer.")
        return None


def normalize_numeric(
    value: Any,
    code: str,
    field: str,
    warnings: list[str],
) -> float | None:
    text = clean_text(value)

    if text is None:
        return None

    normalized_text = text.replace(",", ".")

    try:
        return float(normalized_text)
    except ValueError:
        warnings.append(f"{code}: {field}='{text}' could not be converted to numeric.")
        return None


def normalize_date(value: Any, code: str, warnings: list[str]) -> str | None:
    text = clean_text(value)

    if text is None:
        return None

    # Excel serial date, based on 1899-12-30 convention.
    if re.fullmatch(r"\d+(\.0+)?", text):
        try:
            serial = int(float(text))
            if 1 <= serial <= 60000:
                return (date(1899, 12, 30) + timedelta(days=serial)).isoformat()
        except ValueError:
            pass

    date_formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%d-%m-%Y",
        "%Y/%m/%d",
        "%m/%d/%Y",
    ]

    for date_format in date_formats:
        try:
            return datetime.strptime(text, date_format).date().isoformat()
        except ValueError:
            continue

    warnings.append(f"{code}: sample_date='{text}' could not be converted to date.")
    return None


def clean_text(value: Any) -> str | None:
    if value is None:
        return None

    text = str(value).replace("\u00a0", " ").strip()

    if text == "":
        return None

    return text


def upsert_samples(
    supabase_url: str,
    service_role_key: str,
    rows: list[dict[str, Any]],
) -> None:
    endpoint = f"{supabase_url}/rest/v1/{TABLE_NAME}?on_conflict=code"
    payload = json.dumps(rows, ensure_ascii=False).encode("utf-8")

    headers = {
        "apikey": service_role_key,
        "Content-Type": "application/json",
        "Prefer": "resolution=merge-duplicates,return=minimal",
    }

    # Legacy service_role key is a JWT and can be used as Bearer token.
    # New sb_secret_* key should be sent as API key, not as a user bearer token.
    if service_role_key.startswith("eyJ"):
        headers["Authorization"] = f"Bearer {service_role_key}"

    request = Request(
        endpoint,
        data=payload,
        method="POST",
        headers=headers,
    )

    try:
        with urlopen(request, timeout=60) as response:
            if response.status not in {200, 201, 204}:
                raise RuntimeError(f"Unexpected Supabase response status: {response.status}")
    except HTTPError as error:
        error_body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Supabase HTTP error {error.code}: {error_body}"
        ) from error
    except URLError as error:
        raise RuntimeError(f"Supabase connection error: {error}") from error


def chunked(items: list[dict[str, Any]], size: int) -> list[list[dict[str, Any]]]:
    return [items[index : index + size] for index in range(0, len(items), size)]


def to_repo_path(path: Path) -> str:
    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"\nImport failed: {error}", file=sys.stderr)
        raise SystemExit(1)