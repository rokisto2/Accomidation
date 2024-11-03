from sqlalchemy import Column, Integer, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from .base import Base


class Violation(Base):
    __tablename__ = 'violations'

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'), nullable=False)
    description = Column(Text, nullable=False)
    violation_date = Column(Date, nullable=False)

    # Связь со студентом
    student = relationship('Student', back_populates='violations')

    def __repr__(self):
        return f"<Violation(id={self.id}, student_id={self.student_id}, date={self.violation_date})>"
