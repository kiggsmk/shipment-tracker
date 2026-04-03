from fastapi import FastAPI
from app.api.routes import router
from app.db.session import engine
from app.db.models import Base

app = FastAPI(title="Tracking Service")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

app.include_router(router)