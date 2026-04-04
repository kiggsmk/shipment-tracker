from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_current_user
from app.db.session import SessionLocal
from app.schemas.shipment import ShipmentCreate, ShipmentResponse
from app.services import shipment_service

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.post("/shipments", response_model=ShipmentResponse)
def create_shipment(
    data: ShipmentCreate,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        return shipment_service.create_shipment(db, user, data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/shipments", response_model=list[ShipmentResponse])
def get_shipments(
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return shipment_service.get_all_shipments(db, user)


@router.get("/shipments/{shipment_id}", response_model=ShipmentResponse)
def get_shipment(
    shipment_id: str,
    user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    shipment = shipment_service.get_shipment_by_id(db, shipment_id, user)

    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")

    return shipment