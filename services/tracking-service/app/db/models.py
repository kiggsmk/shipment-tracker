from sqlalchemy import Column, String, TIMESTAMP, Double, BigInteger
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class GPSLog(Base):
    __tablename__ = "gps_logs"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    device_id = Column(String)
    latitude = Column(Double)
    longitude = Column(Double)
    timestamp = Column(TIMESTAMP, server_default=func.now())


class LatestLocation(Base):
    __tablename__ = "latest_location"

    device_id = Column(String, primary_key=True)
    latitude = Column(Double)
    longitude = Column(Double)
    timestamp = Column(TIMESTAMP)