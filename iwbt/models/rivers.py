"""
    River Module contains class River
    Interacts with database for creating, accessing, and updating entries in Iwbt.Rivers
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from iwbt.models import Base


class Area(Base):
    __tablename__ = 'Areas'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<Area: %r>" % self.name


class Gauge(Base):
    __tablename__ = 'Gauges'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    river_id = Column(Integer, ForeignKey('Rivers.id'))
    url = Column(String(128))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<Gauge: %r>" % self.name


class GaugeData(Base):
    __tablename__ = 'GaugeData'
    id = Column(Integer, primary_key=True)
    gauge_id = Column(Integer, ForeignKey('Gauges.id'))
    timestamp = Column(DateTime, default=datetime.now)
    level = Column(Float)
    flow_cfs = Column(Float)

    def __repr__(self):
        return "<GaugeData: %r (%r)>" % (self.gauge.name, self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))


class Rapid(Base):
    __tablename__ = 'Rapids'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    river_id = Column(Integer, ForeignKey('Rivers.id'), nullable=False)
    section_id = Column(Integer, ForeignKey('Sections.id'), nullable=False)
    rating = Column(Float)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    river = relationship('River', backref='rapids', uselist=False)
    section = relationship('Section', backref='rapids', uselist=False)

    def __repr__(self):
        return "<Rapid: %r on %r>" % (self.name, self.river.name)


class River(Base):
    __tablename__ = 'Rivers'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    area_id = Column(Integer, ForeignKey('Areas.id'))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    area = relationship('Area', backref='rivers', uselist=False)

    def __repr__(self):
        return "<River: %r>" % (self.name)


class Section(Base):
    __tablename__ = 'Sections'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    area_id = Column(Integer, ForeignKey('Areas.id'))
    river_id = Column(Integer, ForeignKey('Rivers.id'), nullable=False)
    gauge_id = Column(Integer, ForeignKey('Gauges.id'))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    area = relationship('Area', backref='sections', uselist=False)
    gauge = relationship('Gauge', backref='sections', uselist=False)
    river = relationship('River', backref='sections', uselist=False)

    def __repr__(self):
        return "<Section: %r %r>" % (self.river.name, self.name)