from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Floor(Base):
    __tablename__ = 'floors'

    id = Column(Integer, primary_key=True)
    dormitory_id = Column(Integer, ForeignKey('dormitories.id'), nullable=False)
    floor_number = Column(Integer, nullable=False)

    dormitory = relationship('Dormitory', back_populates='floors')
    rooms = relationship('Room', back_populates='floor', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Floor(id={self.id}, dormitory_id={self.dormitory_id}, floor_number={self.floor_number})>"