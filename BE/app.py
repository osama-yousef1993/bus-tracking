from fastapi import FastAPI
from src.utils.app_routers import setup_routers

app = FastAPI(
    title="Bus Tracking API",
    version="1.0.0",
    description="API for tracking buses in real-time.",
)
setup_routers(app)


@app.get("/")
def root():
    return {"message": "Bus here"}
