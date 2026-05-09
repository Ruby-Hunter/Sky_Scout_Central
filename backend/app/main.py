from endpoints import health, weather
from fastapi import FastAPI

app = FastAPI()

app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
