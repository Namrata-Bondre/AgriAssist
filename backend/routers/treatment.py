"""Treatment recommendation endpoint."""

from fastapi import APIRouter, HTTPException, status

from backend.schemas.recommendation import RecommendationRequest, TreatmentResponse
from backend.services.treatment_service import get_treatment_recommendation

router = APIRouter(prefix="/api", tags=["Treatment"])


@router.post("/treatment", response_model=TreatmentResponse, status_code=status.HTTP_200_OK)
async def treatment(payload: RecommendationRequest) -> TreatmentResponse:
    """Return treatment and prevention guidance for a crop/disease pair."""
    if not payload.crop.strip() or not payload.disease.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Both 'crop' and 'disease' fields are required.",
        )

    try:
        result = get_treatment_recommendation(payload.crop, payload.disease)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate treatment recommendation: {exc}",
        ) from exc

    return TreatmentResponse(
        success=True,
        crop=payload.crop,
        disease=payload.disease,
        treatment=result["treatment"],
        prevention=result["prevention"],
    )
