from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .base import Base
import enum

class RoomTypeEnum(enum.Enum):
    male = "male"
    female = "female"
    family = "family"

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    floor_id = Column(Integer, ForeignKey('floors.id'), nullable=False)
    room_number = Column(Integer, nullable=False)
    room_type = Column(Enum(RoomTypeEnum), nullable=False)
    bed_count = Column(Integer, nullable=False)
    occupied_beds = Column(Integer, default=0)

    floor = relationship('Floor', back_populates='rooms')
    accommodations = relationship('Accommodation', back_populates='room', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Room(id={self.id}, floor_id={self.floor_id}, room_number={self.room_number}, bed_count={self.bed_count})>"