""" Social Media Component of IWBT
    ------------------------------
"""
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Boolean, Column, Date, DateTime, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from . import Base, Model
from . rivers import associate_user_favorites


trip_members = Table('TripMembers', Base.metadata,
                     Column('id', Integer, primary_key=True),
                     Column('user_id', Integer, ForeignKey('Users.id')),
                     Column('trip_id', Integer, ForeignKey('Trips.id'))
                     )


class PaddleLogEntry(Base, Model):
    __tablename__ = 'PaddleLogEntries'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('Users.id'))
    trip_id = Column(Integer, ForeignKey('Trips.id'))
    river_id = Column(Integer, ForeignKey('Rivers.id'))
    section_id = Column(Integer, ForeignKey('Sections.id'))
    public = Column(Boolean, default=False)

    user = relationship('User', backref='paddle_log', uselist=False)
    trip = relationship('Trip', backref='log_entries', uselist=False)

    @property
    def json(self):
        json = self.shallow_json
        json['user'] = self.user.shallow_json
        json['trip'] = self.trip.shallow_json
        return json

    def __repr__(self):
        return "<PaddleLogEntry: %r - %r>" % (self.user.name, self.trip.trip_date.strftime('%Y-%m-%d'))


class Trip(Base, Model):
    __tablename__ = 'Trips'
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    river_id = Column(Integer, ForeignKey('Rivers.id'))
    section_id = Column(Integer, ForeignKey('Sections.id'))
    trip_date = Column(Date, nullable=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    members = relationship('User', secondary=trip_members, backref='trips')
    river = relationship('River', backref='trips', uselist=False)
    section = relationship('Section', backref='trips', uselist=False)

    def __repr__(self):
        return "<Trip: %r (%r) on %r>" % (self.river.name, self.section.name, self.trip_date.strftime('%Y-%m-%d'))


class User(Base, Model, UserMixin):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    alias = Column(String(64), nullable=False)
    password_hash = Column(String(128))
    first_name = Column(String(32))
    last_name = Column(String(32))
    email = Column(String(64))
    moderator = Column(Boolean, default=False)
    admin = Column(Boolean, default=False)
    created = Column(DateTime, default=datetime.now)
    updated = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    favorite_rivers = relationship('River', secondary=associate_user_favorites)

    @property
    def json(self):
        json = self.shallow_json
        return json

    @property
    def shallow_json(self):
        return {k: v for k, v in self.__dict__.iteritems() if k not in ["_sa_instance_state", "password_hash"]}

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute!')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: %r>" % self.alias

