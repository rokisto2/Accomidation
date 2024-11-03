from sqlalchemy import Column, Integer, String
from .base import Base

class User(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(50), nullable=False)
    contact_info = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(100), nullable=False)