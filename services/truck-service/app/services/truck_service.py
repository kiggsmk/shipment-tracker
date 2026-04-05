from sqlalchemy.orm import Session
from app.db.models import Truck

def create_truck(db: Session, user_id: str, truck_id: str, device_id: str):
    truck = Truck(
        truck_id=truck_id,
        user_id=user_id,
        device_id=device_id
    )

    db.add(truck)
    db.commit()
    db.refresh(truck)

    return truck


def get_trucks(db: Session, user_id: str):
    return db.query(Truck).filter(Truck.user_id == user_id).all()


def get_truck_by_id(db: Session, user_id: str, truck_id: str):
    return db.query(Truck).filter(
        Truck.truck_id == truck_id,
        Truck.user_id == user_id
    ).first()