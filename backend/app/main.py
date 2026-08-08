from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.supabase_rest import (
    build_result_payload,
    fetch_images_by_sample_id,
    fetch_sample_by_code,
)


app = FastAPI(
    title="LCGC Backend API",
    version="0.1.0",
    description="Backend API for Laterite Comparator for Grade Control.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "app": "LCGC Backend API",
        "status": "running",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
    }


@app.get("/api/comparator")
def get_comparator(
    code: str = Query(..., description="Comparator sample code, example: BG1 - 01"),
) -> dict:
    settings = get_settings()

    sample = fetch_sample_by_code(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        code=code,
    )

    if sample is None:
        raise HTTPException(status_code=404, detail=f"Sample not found: {code}")

    images = fetch_images_by_sample_id(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        sample_id=sample["id"],
    )

    return {
        "sample": sample,
        "images": images,
    }


@app.get("/api/analysis/mock")
def get_mock_analysis(
    code: str = Query("BG1 - 01", description="Comparator sample code"),
) -> dict:
    settings = get_settings()

    sample = fetch_sample_by_code(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        code=code,
    )

    if sample is None:
        raise HTTPException(status_code=404, detail=f"Sample not found: {code}")

    images = fetch_images_by_sample_id(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        sample_id=sample["id"],
    )

    return build_result_payload(sample, images)