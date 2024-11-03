from models import DeaneryStaff
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class DeaneryStaffRepository:
    def __init__(self, session):
        self.session = session

    def get_deanery_staff_by_username(self, username: str):
        return self.session.query(DeaneryStaff).filter_by(contact_info=username).first()

    def add_deanery_staff(self, first_name, last_name, contact_info, password):
        hashed_password = pwd_context.hash(password)
        deanery_staff = DeaneryStaff(
            first_name=first_name,
            last_name=last_name,
            contact_info=contact_info,
            hashed_password=hashed_password
        )
        self.session.add(deanery_staff)
        self.session.commit()

    def get_all_deanery_staff(self):
        return self.session.query(DeaneryStaff).all()

    def get_deanery_staff_by_id(self, staff_id):
        return self.session.query(DeaneryStaff).get(staff_id)

    def get_deanery_staff_by_contact_info(self, contact_info: str) -> DeaneryStaff:
        return self.session.query(DeaneryStaff).filter(DeaneryStaff.contact_info == contact_info).first()

    def update_deanery_staff(self, staff_id, **kwargs):
        staff = self.get_deanery_staff_by_id(staff_id)
        if staff:
            for key, value in kwargs.items():
                setattr(staff, key, value)
            self.session.commit()

    def delete_deanery_staff(self, staff_id):
        staff = self.get_deanery_staff_by_id(staff_id)
        if staff:
            self.session.delete(staff)
            self.session.commit()