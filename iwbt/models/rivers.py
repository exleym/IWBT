"""
    River Module contains class River
    Interacts with dataBase, Model for creating, accessing, and updating entries in Iwbt.Rivers
"""
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship
from . import Base, Model


associate_user_favorites = Table('FavoriteRivers', Base.metadata,
                                 Column('id', Integer, primary_key=True),
                                 Column('user_id', Integer, ForeignKey('Users.id')),
                                 Column('river_id', Integer, ForeignKey('Rivers.id')))


class Area(Base, Model):
    __tablename__ = 'Areas'
    __table_args__ = (UniqueConstraint('name', name='_area_name_uc'),)
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    rivers = relationship('River', backref='area', uselist=False,
                          cascade="all, delete, delete-orphan")

    sections = relationship('Section', backref='area', uselist=False,
                            cascade="all, delete, delete-orphan")

    def __repr__(self):
        return "<Area: %r>" % self.name


class Gauge(Base, Model):
    __tablename__ = 'Gauges'
    id = Column(Integer, primary_key=True)
    usgs_id = Column(Integer, nullable=True)
    name = Column(String(64), nullable=False)
    river_id = Column(Integer, ForeignKey('Rivers.id'))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    river = relationship('River', backref='gauges', uselist=False)
    data = relationship('GaugeData', backref="gauge", order_by="desc(GaugeData.timestamp)")

    @property
    def current_level(self):
        return self.data[0]

    def get_current_flow(self, flow_type='level'):
        """ method to get current flow from USGS.
        :param flow_type: 'level' or 'flow' -- return level in feet or flow in CFS """
        return 100

    def __repr__(self):
        return "<Gauge: %r>" % self.name


class GaugeData(Base, Model):
    __tablename__ = 'GaugeData'
    __table_args__ = (UniqueConstraint('gauge_id', 'timestamp', name="UQ_GaugeData_gauge_id__timestamp"), )
    id = Column(Integer, primary_key=True)
    gauge_id = Column(Integer, ForeignKey('Gauges.id'))
    timestamp = Column(DateTime, default=datetime.now)
    retrieved = Column(DateTime, default=datetime.now)
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

    def __repr__(self):
        return "<Rapid: %r on %r>" % (self.name, self.river.name)


class River(Base, Model):
    __tablename__ = 'Rivers'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    area_id = Column(Integer, ForeignKey('Areas.id'))
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    rapids = relationship('Rapid', backref='river', uselist=False,
                          cascade="all, delete, delete-orphan")
    sections = relationship('Section', backref='river', uselist=False,
                            cascade="all, delete, delete-orphan")

    @property
    def primary_gauge(self):
        if self.gauges:
            return self.gauges[0]
        else:
            return None

    @property
    def json(self):
        json = {k: v for k, v in self.__dict__.iteritems() if k not in "_sa_instance_state"}
        if self.area:
            json['area'] = self.area.shallow_json
        if self.rapids:
            json['rapids'] = [r.shallow_json for r in self.rapids]
        if self.primary_gauge:
            json['gauge'] = self.primary_gauge.shallow_json
        return json

    @property
    def current_data(self):
        if self.primary_gauge:
            return {'level': self.primary_gauge.current_level.level,
                    'flow': self.primary_gauge.current_level.flow_cfs,
                    'timestamp': self.primary_gauge.current_level.timestamp }
        return {'flow': None, 'level': None, 'timestamp': datetime.now()}

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

    rapids = relationship('Rapid', backref='section', uselist=False,
                          cascade="all, delete, delete-orphan")
    gauge = relationship('Gauge', backref='sections', uselist=False)

    def __repr__(self):
        return "<Section: %r %r>" % (self.river.name, self.name)
