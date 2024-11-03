from sqlalchemy import Column, Integer, ForeignKey, Date
from sqlalchemy.orm import relationship
from .base import Base

class Accommodation(Base):
    __tablename__ = 'accommodations'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id', ondelete='CASCADE'), nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=True)

    # Связь со студентом
    student = relationship('Student', back_populates='accommodations')

    # Связь с комнатой
    room = relationship('Room', back_populates='accommodations')

    def __repr__(self):
        return f"<Accommodation(id={self.id}, student_id={self.student_id}, room_id={self.room_id})>"