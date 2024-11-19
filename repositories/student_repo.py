from sqlalchemy import func

from models import Student, Violation, Accommodation
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class StudentRepository:
    def __init__(self, session):
        self.session = session

    def add_student(self, first_name, last_name, birth_date, contact_info, course, grup, is_non_local, password, gender):
        hashed_password = pwd_context.hash(password)
        student = Student(
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date,
            contact_info=contact_info,
            course=course,
            grup = grup,
            is_non_local=is_non_local,
            hashed_password=hashed_password,
            gender=gender
        )
        self.session.add(student)
        self.session.commit()

    def get_all_students(self):
        return self.session.query(Student).all()

    def get_student_by_id(self, student_id):
        return self.session.query(Student).get(student_id)

    def get_student_by_username(self, username: str) -> Student:
        return self.session.query(Student).filter(Student.contact_info == username).first()

    def update_student(self, student_id, **kwargs):
        student = self.get_student_by_id(student_id)
        if student:
            for key, value in kwargs.items():
                setattr(student, key, value)
            self.session.commit()

    def delete_student(self, student_id):
        student = self.get_student_by_id(student_id)
        if student:
            self.session.delete(student)
            self.session.commit()

    def get_sorted_students(self):
        return self.session.query(
            Student,
            func.count(Violation.id).label('violation_count')
            ).outerjoin(Violation, Student.id == Violation.student_id).group_by(Student.id).order_by(Student.course,'violation_count').all()

    def get_unassigned_students(self):
        subquery = self.session.query(Accommodation.student_id).subquery()
        unassigned_students = self.session.query(Student).filter(Student.id.notin_(subquery)).all()
        print(unassigned_students)
        return unassigned_students