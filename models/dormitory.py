from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from .base import Base

class Dormitory(Base):
    __tablename__ = 'dormitories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    description = Column(Text)

    floors = relationship('Floor', back_populates='dormitory', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Dormitory(id={self.id}, name={self.name})>"