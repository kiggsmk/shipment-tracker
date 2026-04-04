from pydantic import BaseModel

class ShipmentCreate(BaseModel):
    truck_id: str
    origin: str
    destination: str

class ShipmentResponse(BaseModel):
    shipment_id: str
    truck_id: str
    user_id: str
    origin: str
    destination: str
    status: str

    class Config:
        from_attributes = True