from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.tracking import LocationUpdate
from app.services.tracking_service import update_location, get_location_by_shipment
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/tracking/location")
def update_location_api(
    req: LocationUpdate,
    db: Session = Depends(get_db)
):
    return update_location(db, req)


@router.get("/tracking/{shipment_id}")
def track_shipment(shipment_id: str, db: Session = Depends(get_db)):
    loc = get_location_by_shipment(db, shipment_id)

    if not loc:
        raise HTTPException(status_code=404, detail="Location not found")

    return {
        "latitude": loc[0],
        "longitude": loc[1]
    }