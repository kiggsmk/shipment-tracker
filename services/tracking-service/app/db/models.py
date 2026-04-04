from sqlalchemy import Column, String, Float, BigInteger, TIMESTAMP
from sqlalchemy.sql import func
from app.db.session import Base


class GPSLog(Base):
    __tablename__ = "gps_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    device_id = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(TIMESTAMP, server_default=func.now())


class LatestLocation(Base):
    __tablename__ = "latest_location"

    device_id = Column(String, primary_key=True, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    timestamp = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())