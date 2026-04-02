from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.truck import TruckCreate
from app.services.truck_service import create_truck, get_trucks, get_truck_by_id
from app.core.deps import get_current_user
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/trucks")
def create_truck_api(
    req: TruckCreate,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_truck(db, user_id, req.truck_id, req.device_id)


@router.get("/trucks")
def get_trucks_api(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_trucks(db, user_id)


@router.get("/trucks/{truck_id}")
def get_truck_api(
    truck_id: str,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    truck = get_truck_by_id(db, user_id, truck_id)

    if not truck:
        raise HTTPException(status_code=404, detail="Truck not found")

    return truck