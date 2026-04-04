import httpx
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.db.models import GPSLog, LatestLocation
from app.schemas.tracking import LocationUpdateRequest
from app.core.config import settings
from datetime import datetime


class TrackingService:
    def __init__(self, db: Session):
        self.db = db

    def update_location(self, payload: LocationUpdateRequest):
        # 1. Insert into gps_logs
        gps_log = GPSLog(
            device_id=payload.device_id,
            latitude=payload.latitude,
            longitude=payload.longitude,
        )
        self.db.add(gps_log)

        # 2. Upsert latest_location
        existing = (
            self.db.query(LatestLocation)
            .filter(LatestLocation.device_id == payload.device_id)
            .first()
        )

        if existing:
            existing.latitude = payload.latitude
            existing.longitude = payload.longitude
            existing.timestamp = datetime.utcnow()
        else:
            new_location = LatestLocation(
                device_id=payload.device_id,
                latitude=payload.latitude,
                longitude=payload.longitude,
            )
            self.db.add(new_location)

        self.db.commit()

    async def get_location_by_shipment(self, shipment_id: str, token: str):
        headers = {"Authorization": token}

        # 1. Call Shipment Service
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                shipment_res = await client.get(
                    f"{settings.SHIPMENT_SERVICE_URL}/shipments/{shipment_id}",
                    headers=headers,
                )
            except Exception:
                raise HTTPException(status_code=503, detail="Shipment service unavailable")

        if shipment_res.status_code != 200:
            raise HTTPException(status_code=404, detail="Shipment not found")

        shipment_data = shipment_res.json()
        truck_id = shipment_data.get("truck_id")

        # 2. Call Truck Service
        async with httpx.AsyncClient(timeout=5.0) as client:
            try:
                truck_res = await client.get(
                    f"{settings.TRUCK_SERVICE_URL}/trucks/{truck_id}",
                    headers=headers,
                )
            except Exception:
                raise HTTPException(status_code=503, detail="Truck service unavailable")

        if truck_res.status_code != 200:
            raise HTTPException(status_code=404, detail="Truck not found")

        truck_data = truck_res.json()
        device_id = truck_data.get("device_id")

        # 3. Fetch latest location
        location = (
            self.db.query(LatestLocation)
            .filter(LatestLocation.device_id == device_id)
            .first()
        )

        if not location:
            raise HTTPException(status_code=404, detail="Location not found")

        return {
            "device_id": device_id,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "timestamp": location.timestamp,
        }