from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.api.routes import router
from app.db.session import engine
from app.db.models import Base
from app.db.models import Truck  # ✅ IMPORTANT


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Truck tables created")
    yield


app = FastAPI(title="Truck Service", lifespan=lifespan)

app.include_router(router)


@app.get("/health")
def health():
    return {"status": "ok"}