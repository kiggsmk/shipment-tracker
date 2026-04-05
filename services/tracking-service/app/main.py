from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router as tracking_router
from app.db.session import engine
from app.db.models import Base

# 🔥 IMPORTANT: import models so tables get created
from app.db.models import GPSLog, LatestLocation


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Tracking tables created")
    yield


app = FastAPI(title="Tracking Service", lifespan=lifespan)

app.include_router(tracking_router, prefix="/tracking", tags=["Tracking"])


@app.get("/")
def health_check():
    return {"status": "Tracking Service Running"}