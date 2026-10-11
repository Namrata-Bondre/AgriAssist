"""Pydantic schemas shared by the treatment and fertilizer endpoints."""

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    crop: str = Field(..., min_length=1, description="Crop name, e.g. 'Corn'")
    disease: str = Field(..., min_length=1, description="Detected disease name, e.g. 'Common Rust'")


class TreatmentResponse(BaseModel):
    success: bool
    crop: str
    disease: str
    treatment: list[str]
    prevention: list[str]


class FertilizerResponse(BaseModel):
    success: bool
    crop: str
    disease: str
    recommended_fertilizers: list[str]
    nutrient_notes: list[str]
