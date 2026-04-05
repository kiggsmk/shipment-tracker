from fastapi import FastAPI
from app.api.routes import router
from contextlib import asynccontextmanager
from app.db.models import User
from app.db.session import engine
from app.db.models import Base
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    print("Tables created")
    yield  

app = FastAPI(title="Auth Service", lifespan=lifespan)

app.include_router(router)


    
@app.get("/health")
def health():
    return {"status": "ok"}