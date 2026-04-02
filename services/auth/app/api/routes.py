from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import SignupRequest, LoginRequest
from app.services.auth_service import create_user, authenticate_user
from app.db.session import SessionLocal
from app.core.deps import get_current_user

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/auth/signup")
def signup(req: SignupRequest, db: Session = Depends(get_db)):
    user = create_user(db, req.email, req.password)

    if not user:
        raise HTTPException(status_code=400, detail="User already exists")

    return {"user_id": str(user.user_id)}

@router.post("/auth/login")
def login(req: LoginRequest, db: Session = Depends(get_db)):
    token = authenticate_user(db, req.email, req.password)

    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token}


@router.get("/auth/me")
def get_me(user_id: str = Depends(get_current_user)):
    return {
        "message": "Authenticated user",
        "user_id": user_id
    }