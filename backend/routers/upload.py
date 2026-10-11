"""Image upload endpoint."""

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from backend.schemas.prediction import UploadResponse
from backend.utils.file_utils import (
    get_relative_static_path,
    is_allowed_file,
    save_upload_file,
)

router = APIRouter(prefix="/api", tags=["Upload"])


@router.post("/upload", response_model=UploadResponse, status_code=status.HTTP_200_OK)
async def upload_image(file: UploadFile = File(...)) -> UploadResponse:
    """Upload a leaf image (JPG, JPEG, PNG) and store it on the server."""
    if not file or not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No file was provided.")

    if not is_allowed_file(file.filename, file.content_type):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Only JPG, JPEG, and PNG images are allowed.",
        )

    try:
        unique_filename, _absolute_path = await save_upload_file(file)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save uploaded file: {exc}",
        ) from exc

    return UploadResponse(
        success=True,
        filename=unique_filename,
        filepath=get_relative_static_path(unique_filename),
        message="Image uploaded successfully",
    )
