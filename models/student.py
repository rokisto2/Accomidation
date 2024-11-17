from sqlalchemy import Column, Integer, Date, Boolean, Enum
from sqlalchemy.orm import relationship
from .base import Base
from .user import User
import enum

class GenderEnum(enum.Enum):
    male = "male"
    female = "female"

class Student(User):
    __tablename__ = 'students'

    birth_date = Column(Date)
    course = Column(Integer)
    grup = Column(Integer)
    is_non_local = Column(Boolean, default=False)
    gender = Column(Enum(GenderEnum), nullable=False)

    # Relationship with violations
    violations = relationship('Violation', back_populates='student')

    # Relationship with accommodations
    accommodations = relationship('Accommodation', back_populates='student')

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.first_name} {self.last_name}, course={self.course})>"