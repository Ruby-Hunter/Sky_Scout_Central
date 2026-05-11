from datetime import datetime
from typing import Annotated

import httpx
import models
from database import get_db
from fastapi import APIRouter, Depends, HTTPException
from schemas import WeatherDataFromAPI, WeatherDataFull, WeatherDataUpload
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


async def fetch_weather_data_from_api(lat: float, lon: float) -> WeatherDataFromAPI:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current="
        "wind_speed_10m,"
        "wind_direction_10m,"
        "weather_code,"
        "precipitation,"
        "uv_index,"
        "visibility,"
        "cloud_base"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    current = data["current"]

    return WeatherDataFromAPI(
        wind_speed=(
            current["wind_speed_10m"] * (1000 / 3600)
            if "wind_speed_10m" in current
            else None
        ),
        wind_direction=(
            current["wind_direction_10m"] if "wind_direction_10m" in current else None
        ),
        weather_code=(current["weather_code"] if "weather_code" in current else None),
        precipitation_cm=(
            current["precipitation"] / 10 if "precipitation" in current else None
        ),
        uv_index=(current["uv_index"] if "uv_index" in current else None),
        render_distance_km=(
            current["visibility"] / 1000 if "visibility" in current else None
        ),
        cloud_height_m=(current["cloud_base"] if "cloud_base" in current else None),
    )


async def fetch_full_weather_data_from_api(lat: float, lon: float) -> WeatherDataFull:
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current="
        "temperature_2m,"
        "relative_humidity_2m,"
        "pressure_msl,"
        "wind_speed_10m,"
        "wind_direction_10m,"
        "weather_code,"
        "precipitation,"
        "uv_index,"
        "visibility,"
        "cloud_base"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

    current = data["current"]

    return WeatherDataFull(
        timestamp=datetime.now(),
        temperature=current["temperature_2m"],
        humidity=current["relative_humidity_2m"],
        pressure=current["pressure_msl"],
        wind_speed=current["wind_speed_10m"] * (1000 / 3600)
        if "wind_speed_10m" in current
        else None,
        wind_direction=current["wind_direction_10m"]
        if "wind_direction_10m" in current
        else None,
        weather_code=current["weather_code"] if "weather_code" in current else None,
        precipitation_cm=current["precipitation"] / 10
        if "precipitation" in current
        else None,
        uv_index=current["uv_index"] if "uv_index" in current else None,
        render_distance_km=current["visibility"] / 1000
        if "visibility" in current
        else None,
        cloud_height_m=current["cloud_base"] if "cloud_base" in current else None,
        cloud_cover_percent=None,
    )


@router.post("/upload")
async def upload_weather_data(
    upload_data: WeatherDataUpload, db: Annotated[Session, Depends(get_db)]
):
    weather_data = await fetch_weather_data_from_api(
        upload_data.latitude, upload_data.longitude
    )
    new_data = models.WeatherData(
        timestamp=upload_data.timestamp,
        temperature=upload_data.temperature,
        humidity=upload_data.humidity,
        pressure=upload_data.pressure,
        wind_speed=weather_data.wind_speed,
        wind_direction=weather_data.wind_direction,
        weather_code=weather_data.weather_code,
        precipitation_cm=weather_data.precipitation_cm,
        uv_index=weather_data.uv_index,
        render_distance_km=weather_data.render_distance_km,
        cloud_height_m=weather_data.cloud_height_m,
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return new_data


@router.post("/fetch_from_coords")
async def fetch_weather_from_coords(
    lat: float, lon: float, db: Annotated[Session, Depends(get_db)]
):
    weather_data = await fetch_full_weather_data_from_api(lat, lon)
    new_data = models.WeatherData(
        timestamp=weather_data.timestamp,
        temperature=weather_data.temperature,
        humidity=weather_data.humidity,
        pressure=weather_data.pressure,
        wind_speed=weather_data.wind_speed,
        wind_direction=weather_data.wind_direction,
        weather_code=weather_data.weather_code,
        precipitation_cm=weather_data.precipitation_cm,
        uv_index=weather_data.uv_index,
        render_distance_km=weather_data.render_distance_km,
        cloud_height_m=weather_data.cloud_height_m,
    )
    db.add(new_data)
    db.commit()
    db.refresh(new_data)
    return weather_data


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
    return {
        "temp": weather_data.temperature,
        "humidity": weather_data.humidity,
        "pressure": weather_data.pressure,
        "wind_speed": weather_data.wind_speed,
        "wind_direction": weather_data.wind_direction,
        "weather_code": weather_data.weather_code,
        "precipitation_cm": weather_data.precipitation_cm,
        "uv_index": weather_data.uv_index,
        "render_distance_km": weather_data.render_distance_km,
        "cloud_height": weather_data.cloud_height_m,
    }
