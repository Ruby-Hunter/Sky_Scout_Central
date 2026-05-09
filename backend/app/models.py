from __future__ import annotations

from datetime import UTC, datetime

from database import Base
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column


class WeatherData(Base):
    __tablename__ = "weather_data"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC), nullable=False
    )
    temperature: Mapped[float] = mapped_column(nullable=False)
    humidity: Mapped[float] = mapped_column(nullable=False)
    pressure: Mapped[float] = mapped_column(nullable=False)
    wind_speed: Mapped[float] = mapped_column(nullable=False)
    wind_direction: Mapped[float] = mapped_column(nullable=True)
    weather_code: Mapped[int] = mapped_column(nullable=False)
    precipitation_cm: Mapped[float] = mapped_column(nullable=True)
    uv_index: Mapped[float] = mapped_column(nullable=False)
    render_distance_km: Mapped[float] = mapped_column(nullable=True)
    cloud_height_m: Mapped[int] = mapped_column(nullable=True)
