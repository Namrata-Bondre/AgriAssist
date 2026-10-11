"""
AgriAssist Backend - FastAPI application entry point.

Run with:
    python -m uvicorn backend.main:app --reload --port 8000
"""

import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

from backend.routers import chatbot, fertilizer, predict, treatment, upload, weather
from backend.utils.file_utils import BASE_DIR, ensure_upload_dir_exists

# Load environment variables from backend/.env
BASE_ENV_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_ENV_DIR, ".env"), override=True)

app = FastAPI(
    title="AgriAssist Backend",
    description="AI Smart Farming Assistant - Backend API",
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# CORS configuration (environment-based)
# ---------------------------------------------------------------------------
allowed_origins_raw = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173")
allowed_origins = [origin.strip() for origin in allowed_origins_raw.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Static files (uploaded images)
# ---------------------------------------------------------------------------
ensure_upload_dir_exists()
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(upload.router)
app.include_router(predict.router)
app.include_router(treatment.router)
app.include_router(fertilizer.router)
app.include_router(chatbot.router)
app.include_router(weather.router)


# ---------------------------------------------------------------------------
# Global error handlers -> clean JSON error responses
# ---------------------------------------------------------------------------
@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"success": False, "error": "Internal server error", "detail": str(exc)},
    )


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.get("/health", tags=["Health"])
async def health_check() -> dict:
    return {"status": "ok", "service": "AgriAssist Backend"}


@app.get("/", tags=["Health"])
async def root() -> dict:
    return {
        "message": "AgriAssist Backend is running",
        "docs": "/docs",
        "redoc": "/redoc",
    }
