from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class WeatherDataBase(BaseModel):
    timestamp: datetime


class WeatherDataFromAPI(BaseModel):
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    weather_code: Optional[int]
    precipitation_cm: Optional[float]
    uv_index: Optional[float]
    render_distance_km: Optional[float]
    cloud_height_m: Optional[int]
    cloud_cover_percent: Optional[int]


class WeatherDataFull(WeatherDataBase):
    temperature: float
    humidity: float
    pressure: float
    wind_speed: Optional[float]
    wind_direction: Optional[float]
    weather_code: Optional[int]
    precipitation_cm: Optional[float]
    uv_index: Optional[float]
    render_distance_km: Optional[float]
    cloud_height_m: Optional[int]
    cloud_cover_percent: Optional[int]


class WeatherDataUpload(WeatherDataBase):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    temperature: float
    humidity: float
    pressure: float


class WeatherDataWithId(WeatherDataFull):
    id: int

    class Config:
        orm_mode = True
