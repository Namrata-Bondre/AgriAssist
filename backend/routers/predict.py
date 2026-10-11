"""Disease prediction endpoint. Delegates to Mona's ML module."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.schemas.prediction import PredictionResponse
from backend.services.ml_service import MLServiceUnavailableError, predict_disease
from backend.utils.file_utils import is_allowed_file, save_upload_file

router = APIRouter(prefix="/api", tags=["Prediction"])


@router.post("/predict", response_model=PredictionResponse, status_code=status.HTTP_200_OK)
async def predict(file: UploadFile = File(...)) -> PredictionResponse:
    """Accept a leaf image and return the predicted crop, disease, and confidence."""
    if not file or not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No image was provided.")

    if not is_allowed_file(file.filename, file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only JPG, JPEG, and PNG images are allowed.",
        )

    try:
        _unique_filename, absolute_path = await save_upload_file(file)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save uploaded image: {exc}",
        ) from exc

    try:
        result = predict_disease(absolute_path)
    except MLServiceUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=exc.message,
        ) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Prediction failed: {exc}",
        ) from exc

    return PredictionResponse(
        success=True,
        crop=result["crop"],
        disease=result["disease"],
        confidence=result["confidence"],
    )
