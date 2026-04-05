from pydantic import BaseModel

class TruckCreate(BaseModel):
    truck_id: str
    device_id: str