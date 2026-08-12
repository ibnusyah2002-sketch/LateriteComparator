from __future__ import annotations

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.ai.similarity import find_best_candidate
from app.config import get_settings
from app.image_input import decode_and_save_data_url, to_backend_relative_path
from app.schemas import AnalysisRequest
from app.supabase_rest import (
    attach_signed_urls_to_images,
    build_result_payload,
    fetch_images_by_sample_id,
    fetch_sample_by_code,
    fetch_samples_by_codes,
)


app = FastAPI(
    title="LCGC Backend API",
    version="0.2.0",
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

@app.get("/api/ai/health")
def ai_health() -> dict[str, str]:
    return {
        "status": "ok",
        "mode": "pre_ai_placeholder",
        "next": "image feature extraction and comparator similarity search",
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

    signed_images = attach_signed_urls_to_images(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        bucket=settings.supabase_storage_bucket,
        images=images,
    )

    return {
        "sample": sample,
        "images": signed_images,
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

    signed_images = attach_signed_urls_to_images(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        bucket=settings.supabase_storage_bucket,
        images=images,
    )

def build_top_candidate_payloads(
    candidate_rows: list[dict],
    ranked_candidates: list[dict],
) -> list[dict]:
    sample_by_code = {
        sample.get("code"): sample
        for sample in candidate_rows
        if sample.get("code")
    }

    payloads: list[dict] = []

    for candidate in ranked_candidates:
        code = candidate.get("code")
        sample = sample_by_code.get(code, {})

        payloads.append(
            {
                "code": code,
                "score": candidate.get("score"),
                "confidence_label": candidate.get("confidence_label"),
                "zone": sample.get("zone"),
                "color": sample.get("color"),
                "description": sample.get("description"),
                "qaqc": {
                    "ni": sample.get("ni"),
                    "co": sample.get("co"),
                    "fe": sample.get("fe"),
                    "sio2": sample.get("sio2"),
                    "mgo": sample.get("mgo"),
                    "fe_ni": sample.get("fe_ni"),
                    "s_m": sample.get("s_m"),
                },
                "local_path": candidate.get("local_path"),
                "storage_path": candidate.get("storage_path"),
            }
        )

    return payloads  

@app.post("/api/analysis")
def post_analysis(request: AnalysisRequest) -> dict:
    settings = get_settings()

    try:
        decoded_image = decode_and_save_data_url(request.image_data_url)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    try:
        best_candidate = find_best_candidate(decoded_image.saved_path)
    except FileNotFoundError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    sample = fetch_sample_by_code(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        code=best_candidate.code,
    )

    if sample is None:
        raise HTTPException(
            status_code=404,
            detail=f"Matched sample not found: {best_candidate.code}",
        )

    images = fetch_images_by_sample_id(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        sample_id=sample["id"],
    )

    signed_images = attach_signed_urls_to_images(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        bucket=settings.supabase_storage_bucket,
        images=images,
    )

    payload = build_result_payload(sample, signed_images)

    candidate_codes = [
        candidate["code"]
        for candidate in best_candidate.ranked_candidates
        if candidate.get("code")
    ]

    candidate_rows = fetch_samples_by_codes(
        supabase_url=settings.supabase_url,
        service_role_key=settings.supabase_service_role_key,
        codes=candidate_codes,
    )

    top_candidates = build_top_candidate_payloads(
        candidate_rows=candidate_rows,
        ranked_candidates=best_candidate.ranked_candidates,
    )

    payload["similarity"] = {
        "score": best_candidate.score,
        "confidence_label": best_candidate.confidence_label,
        "method": best_candidate.method,
        "note": best_candidate.note,
        "top_candidates": top_candidates,
    }

    preprocessing = best_candidate.preprocessing

    payload["analysis_request"] = {
        "source": request.source,
        "image_received": True,
        "image_size_characters": len(request.image_data_url),
        "image_mime_type": decoded_image.mime_type,
        "image_size_bytes": decoded_image.size_bytes,
        "image_saved_path": to_backend_relative_path(decoded_image.saved_path),
        "matched_code": best_candidate.code,
        "mode": best_candidate.method,
        "preprocessing_method": preprocessing.method if preprocessing else None,
        "preprocessed_image_saved_path": (
            to_backend_relative_path(preprocessing.processed_path)
            if preprocessing
            else None
        ),
        "preprocessing_crop_ratio": preprocessing.crop_ratio if preprocessing else None,
        "original_image_size": preprocessing.original_size if preprocessing else None,
        "processed_image_size": preprocessing.processed_size if preprocessing else None,
    }

    return payload

    return build_result_payload(sample, signed_images)