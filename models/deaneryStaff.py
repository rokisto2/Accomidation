# models/deaneryStaff.py
from sqlalchemy import Column, Integer
from .base import Base
from .user import User

class DeaneryStaff(User):
    __tablename__ = 'deanery_staff'


    def __repr__(self):
        return f"<DeaneryStaff(id={self.id}, name={self.first_name} {self.last_name})>"