from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base
from .user import User

class Administration(User):
    __tablename__ = 'administration'

    dormitory_id = Column(Integer, ForeignKey('dormitories.id'), nullable=False)
    contributions = Column(Integer, default=0)

    # Relationship with dormitory
    dormitory = relationship('Dormitory')

    def __repr__(self):
        return f"<Administration(id={self.id}, name={self.first_name} {self.last_name}, contributions={self.contributions})>"