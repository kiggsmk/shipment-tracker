from pydantic import BaseModel
from datetime import datetime


class LocationUpdateRequest(BaseModel):
    device_id: str
    latitude: float
    longitude: float


class LocationResponse(BaseModel):
    device_id: str
    latitude: float
    longitude: float
    timestamp: datetime