from database import Base, engine, get_db
from endpoints import health, weather
from fastapi import FastAPI

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(weather.router, prefix="/api/weather", tags=["weather"])
app.include_router(health.router, prefix="/api/health", tags=["health"])
