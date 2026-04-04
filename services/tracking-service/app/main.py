from fastapi import FastAPI
from app.api.routes import router as tracking_router

app = FastAPI(title="Tracking Service")

app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])


@app.get("/")
def health_check():
    return {"status": "Tracking Service Running"}