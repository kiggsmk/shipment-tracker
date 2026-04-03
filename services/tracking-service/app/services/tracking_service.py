from sqlalchemy.orm import Session
from app.db.models import GPSLog, LatestLocation

def update_location(db: Session, data):
    # 1. insert into gps_logs
    log = GPSLog(
        device_id=data.device_id,
        latitude=data.latitude,
        longitude=data.longitude
    )
    db.add(log)

    # 2. upsert latest_location
    existing = db.query(LatestLocation).filter(
        LatestLocation.device_id == data.device_id
    ).first()

    if existing:
        existing.latitude = data.latitude
        existing.longitude = data.longitude
    else:
        new_loc = LatestLocation(
            device_id=data.device_id,
            latitude=data.latitude,
            longitude=data.longitude
        )
        db.add(new_loc)

    db.commit()

    return {"status": "updated"}


def get_location_by_shipment(db: Session, shipment_id: str):
    result = db.execute(f"""
        SELECT l.latitude, l.longitude
        FROM shipments s
        JOIN trucks t ON s.truck_id = t.truck_id
        JOIN latest_location l ON t.device_id = l.device_id
        WHERE s.shipment_id = '{shipment_id}'
    """)

    return result.fetchone()