"""
    River Module contains class River
    Interacts with dataBase, Model for creating, accessing, and updating entries in Iwbt.Rivers
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from iwbt.models import Base, Model


associate_user_favorites = Table('FavoriteRivers', Base.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('user_id', Integer, ForeignKey('Users.id')),
                                 Column('river_id', Integer, ForeignKey('Rivers.id')))


class Area(Base, Model):
    __tablename__ = 'Areas'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<Area: %r>" % self.name


class Gauge(Base, Model):
    __tablename__ = 'Gauges'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    river_id = Column(Integer, ForeignKey('Rivers.id'))
    url = Column(String(128))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return "<Gauge: %r>" % self.name


class GaugeData(Base, Model):
    __tablename__ = 'GaugeData'
    id = Column(Integer, primary_key=True)
    gauge_id = Column(Integer, ForeignKey('Gauges.id'))
    timestamp = Column(DateTime, default=datetime.now)
    level = Column(Float)
    flow_cfs = Column(Float)

    def __repr__(self):
        return "<GaugeData: %r (%r)>" % (self.gauge.name, self.timestamp.strftime('%Y-%m-%d %H:%M:%S'))


class Rapid(Base, Model):
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


class River(Base, Model):
    __tablename__ = 'Rivers'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    area_id = Column(Integer, ForeignKey('Areas.id'))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    area = relationship('Area', backref='rivers', uselist=False)

    @property
    def json(self):
        json = {k: v for k, v in self.__dict__.iteritems() if k not in "_sa_instance_state"}
        if self.area:
            json['area'] = self.area.shallow_json
        if self.rapids:
            json['rapids'] = [r.shallow_json for r in self.rapids]
        return json

    @property
    def current_flow(self):
        return 550

    def __repr__(self):
        return "<River: %r>" % (self.name)


class Section(Base, Model):
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