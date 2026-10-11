"""
File handling utilities: validation, unique filename generation,
and saving uploaded images to disk.
"""

import os
import uuid
from pathlib import Path

from fastapi import UploadFile

# Allowed image extensions and their corresponding content types
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/jpg", "image/png"}

# Base directory of the backend package (backend/)
BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "static" / "uploads"


def ensure_upload_dir_exists() -> None:
    """Create the uploads directory if it does not already exist."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def is_allowed_file(filename: str, content_type: str | None) -> bool:
    """
    Validate that a file has an allowed image extension and,
    if provided, an allowed content type.
    """
    if not filename:
        return False

    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        return False

    if content_type is not None and content_type.lower() not in ALLOWED_CONTENT_TYPES:
        return False

    return True


def generate_unique_filename(original_filename: str) -> str:
    """Generate a unique filename while preserving the original extension."""
    extension = Path(original_filename).suffix.lower()
    unique_name = f"{uuid.uuid4().hex}{extension}"
    return unique_name


async def save_upload_file(upload_file: UploadFile) -> tuple[str, str]:
    """
    Save an UploadFile to the static/uploads directory using a unique filename.

    Returns:
        tuple: (unique_filename, absolute_file_path_as_string)
    """
    ensure_upload_dir_exists()

    unique_filename = generate_unique_filename(upload_file.filename)
    destination_path = UPLOAD_DIR / unique_filename

    contents = await upload_file.read()
    with open(destination_path, "wb") as buffer:
        buffer.write(contents)

    # Reset pointer in case the file object is reused elsewhere
    await upload_file.seek(0)

    return unique_filename, str(destination_path)


def get_relative_static_path(filename: str) -> str:
    """Return the path used in API responses, relative to the backend root."""
    return f"static/uploads/{filename}"
