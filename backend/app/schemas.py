from datetime import datetime

from pydantic import BaseModel, Field


class WeatherDataBase(BaseModel):
    timestamp: datetime


class WeatherDataFull(WeatherDataBase):
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float
    wind_direction: float
    weather_code: int
    precipitation_cm: float
    uv_index: float
    render_distance_km: float
    cloud_height_m: int
    cloud_cover_percent: int


class WeatherDataUpload(WeatherDataBase):
    temperature: float
    humidity: float
    pressure: float


class WeatherData(WeatherDataFull):
    id: int

    class Config:
        orm_mode = True
