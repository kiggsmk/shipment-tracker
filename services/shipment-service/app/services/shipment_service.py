import uuid
from sqlalchemy.orm import Session

from app.db.models import Shipment
from app.clients.truck_client import validate_truck_ownership


def create_shipment(db: Session, user, data):
    user_id = user["user_id"]
    token = user["token"]

    # 🔥 REAL validation with Truck Service
    is_valid = validate_truck_ownership(data.truck_id, user_id, token)

    if not is_valid:
        raise Exception("Truck does not belong to user or service unavailable")

    shipment = Shipment(
        shipment_id=str(uuid.uuid4()),
        truck_id=data.truck_id,
        user_id=user_id,
        origin=data.origin,
        destination=data.destination
    )

    db.add(shipment)
    db.commit()
    db.refresh(shipment)

    return shipment


def get_all_shipments(db: Session, user):
    return db.query(Shipment).filter(
        Shipment.user_id == user["user_id"]
    ).all()


def get_shipment_by_id(db: Session, shipment_id: str, user):
    return db.query(Shipment).filter(
        Shipment.shipment_id == shipment_id,
        Shipment.user_id == user["user_id"]
    ).first()