from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.tracking import LocationUpdateRequest, LocationResponse
from app.services.tracking_service import TrackingService

router = APIRouter()


@router.post("/location")
def update_location(
    payload: LocationUpdateRequest,
    db: Session = Depends(get_db),
):
    service = TrackingService(db)
    service.update_location(payload)
    return {"message": "Location updated successfully"}


@router.get("/{shipment_id}", response_model=LocationResponse)
async def get_tracking(
    shipment_id: str,
    db: Session = Depends(get_db),
    authorization: str = Header(None),
):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    service = TrackingService(db)

    return await service.get_location_by_shipment(
        shipment_id=shipment_id,
        token=authorization,
    )