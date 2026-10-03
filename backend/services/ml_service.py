"""
ML integration service.

This module does NOT implement or train any machine learning model.
It only provides a clean bridge to Mona's ML module, which is expected
to live at: backend/ml/predict.py and expose a function:

    predict_image(image_path: str) -> dict

Expected return shape from Mona's predict_image():
    {
        "crop": "Corn",
        "disease": "Common Rust",
        "confidence": 98.45
    }

If Mona's ML files are not yet present, this service raises a clear,
descriptive MLServiceUnavailableError instead of crashing the app.
"""

import importlib
import importlib.util
from pathlib import Path
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent
ML_DIR = BASE_DIR / "ml"
ML_PREDICT_MODULE_PATH = ML_DIR / "predict.py"
ML_MODEL_PATH = ML_DIR / "fine_tuned_best.keras"
ML_CLASS_MAPPING_PATH = ML_DIR / "class_mapping.json"


class MLServiceUnavailableError(Exception):
    """Raised when Mona's ML module or model files are not available."""

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


def _check_ml_files_present() -> list[str]:
    """Return a list of human-readable messages for any missing ML files."""
    missing = []
    if not ML_PREDICT_MODULE_PATH.exists():
        missing.append("backend/ml/predict.py is missing")
    if not ML_MODEL_PATH.exists():
        missing.append("backend/ml/fine_tuned_best.keras is missing")
    if not ML_CLASS_MAPPING_PATH.exists():
        missing.append("backend/ml/class_mapping.json is missing")
    return missing


def _load_predict_function():
    """
    Dynamically load Mona's predict_image function from backend/ml/predict.py.

    We do NOT reimplement or modify her code. We only import it.
    """
    missing = _check_ml_files_present()
    if missing:
        raise MLServiceUnavailableError(
            "ML module is not available yet. Missing: " + "; ".join(missing)
        )

    spec = importlib.util.spec_from_file_location("mona_predict", ML_PREDICT_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise MLServiceUnavailableError(
            "Could not load backend/ml/predict.py. Please verify the file is valid Python."
        )

    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001
        raise MLServiceUnavailableError(
            f"Failed to import backend/ml/predict.py: {exc}"
        ) from exc

    if not hasattr(module, "predict_image"):
        raise MLServiceUnavailableError(
            "backend/ml/predict.py was found but does not define a predict_image() function."
        )

    return module.predict_image


def predict_disease(image_path: str) -> dict[str, Any]:
    """
    Call Mona's predict_image(image_path) and normalize the result.

    Raises:
        MLServiceUnavailableError: if the ML module/files are missing or fail to load.
    """
    predict_image = _load_predict_function()

    try:
        result = predict_image(image_path)
    except Exception as exc:  # noqa: BLE001
        raise MLServiceUnavailableError(
            f"The ML model failed to produce a prediction: {exc}"
        ) from exc

    if not isinstance(result, dict):
        raise MLServiceUnavailableError(
            "predict_image() returned an unexpected format. Expected a dict with "
            "'crop', 'disease', and 'confidence' keys."
        )

    for key in ("crop", "disease", "confidence"):
        if key not in result:
            raise MLServiceUnavailableError(
                f"predict_image() result is missing the '{key}' field."
            )

    return {
        "crop": result["crop"],
        "disease": result["disease"],
        "confidence": float(result["confidence"]),
    }
