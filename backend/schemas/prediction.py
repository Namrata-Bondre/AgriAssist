"""Pydantic schemas for upload and prediction endpoints."""

from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    success: bool
    filename: str
    filepath: str
    message: str


class PredictionResponse(BaseModel):
    success: bool
    crop: str
    disease: str
    confidence: float = Field(..., description="Prediction confidence as a percentage")


class ErrorResponse(BaseModel):
    success: bool = False
    error: str
    detail: str | None = None
