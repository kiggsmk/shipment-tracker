from sqlalchemy import Column, String, TIMESTAMP, text
from app.db.session import Base

class Shipment(Base):
    __tablename__ = "shipments"

    shipment_id = Column(String, primary_key=True, index=True)
    truck_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    origin = Column(String)
    destination = Column(String)
    status = Column(String, default="CREATED")
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))