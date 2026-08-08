from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = BACKEND_ROOT / ".env.local"


@dataclass(frozen=True)
class Settings:
    supabase_url: str
    supabase_service_role_key: str
    supabase_storage_bucket: str


def load_env_file(path: Path) -> dict[str, str]:
    env: dict[str, str] = {}

    if not path.exists():
        return env

    for line in path.read_text(encoding="utf-8").splitlines():
        clean_line = line.strip()

        if not clean_line or clean_line.startswith("#"):
            continue

        if "=" not in clean_line:
            continue

        key, value = clean_line.split("=", 1)
        env[key.strip()] = value.strip().strip('"').strip("'")

    return env


def required_value(env: dict[str, str], key: str) -> str:
    value = os.environ.get(key) or env.get(key)

    if not value:
        raise RuntimeError(f"Missing required environment value: {key}")

    return value


def get_settings() -> Settings:
    env = load_env_file(ENV_PATH)

    return Settings(
        supabase_url=required_value(env, "SUPABASE_URL").rstrip("/"),
        supabase_service_role_key=required_value(env, "SUPABASE_SERVICE_ROLE_KEY"),
        supabase_storage_bucket=required_value(env, "SUPABASE_STORAGE_BUCKET"),
    )