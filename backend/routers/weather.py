"""Weather endpoint (OpenWeatherMap-powered)."""

from fastapi import APIRouter, HTTPException, Query, status
from pydantic import BaseModel

from backend.services.weather_service import WeatherServiceError, get_weather

router = APIRouter(prefix="/api", tags=["Weather"])


class WeatherResponse(BaseModel):
    success: bool
    city: str
    temperature: float
    humidity: int
    description: str
    wind_speed: float


@router.get("/weather", response_model=WeatherResponse, status_code=status.HTTP_200_OK)
async def weather(city: str = Query(..., min_length=1, description="City name, e.g. Indore")) -> WeatherResponse:
    """Return current weather conditions for the given city."""
    if not city.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="City name is required.")

    try:
        data = await get_weather(city)
    except WeatherServiceError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch weather data: {exc}",
        ) from exc

    return WeatherResponse(
        success=True,
        city=data["city"],
        temperature=data["temperature"],
        humidity=data["humidity"],
        description=data["description"],
        wind_speed=data["wind_speed"],
    )
