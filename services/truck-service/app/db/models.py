from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base  # ✅ use shared Base


class Truck(Base):
    __tablename__ = "trucks"

    truck_id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    device_id = Column(String, unique=True, nullable=False)
    status = Column(String, default="ACTIVE")
    created_at = Column(TIMESTAMP, server_default=func.now())