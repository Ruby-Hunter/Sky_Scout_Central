from typing import Annotated

import httpx
import models
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas import WeatherData, WeatherDataFull, WeatherDataUpload
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


async def fetch_weather_data_from_api(lat: float, lon: float):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current="
        "wind_speed_10m"
        "wind_direction_10m"
        "weather_code"
        "precipitation"
        "uv_index"
        "visibility"
        "cloud_base"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    current = data["current"]

    return {
        "wind_speed": current["wind_speed_10m"],
        "wind_direction": current["wind_direction_10m"],
        "weather_code": current["weather_code"],
        "precipitation_cm": current["precipitation"],
        "uv_index": current["uv_index"],
        "render_distance_km": current["visibility"],
        "cloud_height_m": current["cloud_base"],
    }


@router.post("/upload")
def upload_weather_data(
    data: WeatherDataUpload, db: Annotated[Session, Depends(get_db)]
):

    new_data = models.WeatherData(
        timestamp=data.timestamp,
        temperature=data.temperature,
        humidity=data.humidity,
        pressure=data.pressure,
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)


@router.get("/latest")
def get_weather_latest(db: Annotated[Session, Depends(get_db)]):
    result = db.execute(
        select(models.WeatherData)
        .order_by(models.WeatherData.timestamp.desc())
        .limit(1)
    )
    weather_data = result.scalars().first()
    if not weather_data:
        raise HTTPException(
            status_code=404, detail="No weather data found; database may be empty."
        )
    return {"temp": 67, "humidity": 93, "wind_speed": 5, "cloud_height": 1000}
