"""
    Weather Module contains data models for precipitation and associated data
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from iwbt.models import Base, Model


class WeatherStation(Base):
    __tablename__ = 'WeatherStations'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('WeatherSources.id'))
    latitude = Column(Float)
    longitude = Column(Float)