from __future__ import annotations

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    image_data_url: str = Field(
        ...,
        description="Captured or uploaded scan image as data URL.",
    )
    source: str | None = Field(
        default="unknown",
        description="Image source, for example camera or upload.",
    )


class AnalysisResponseMeta(BaseModel):
    mode: str
    note: str