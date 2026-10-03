"""Fertilizer recommendation endpoint."""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.recommendation import FertilizerResponse, RecommendationRequest
from backend.services.fertilizer_service import get_fertilizer_recommendation

router = APIRouter(prefix="/api", tags=["Fertilizer"])


@router.post("/fertilizer", response_model=FertilizerResponse, status_code=status.HTTP_200_OK)
async def fertilizer(payload: RecommendationRequest) -> FertilizerResponse:
    """Return fertilizer and nutrient guidance for a crop/disease pair."""
    if not payload.crop.strip() or not payload.disease.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both 'crop' and 'disease' fields are required.",
        )

    try:
        result = get_fertilizer_recommendation(payload.crop, payload.disease)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate fertilizer recommendation: {exc}",
        ) from exc

    return FertilizerResponse(
        success=True,
        crop=payload.crop,
        disease=payload.disease,
        recommended_fertilizers=result["recommended_fertilizers"],
        nutrient_notes=result["nutrient_notes"],
    )
