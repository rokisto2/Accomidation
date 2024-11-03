from models import Administration
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AdministrationRepository:
    def __init__(self, session):
        self.session = session

    def add_administration(self, first_name, last_name, contact_info, dormitory_id, password, contributions=0):
        hashed_password = pwd_context.hash(password)
        admin = Administration(
            first_name=first_name,
            last_name=last_name,
            contact_info=contact_info,
            dormitory_id=dormitory_id,
            contributions=contributions,
            hashed_password=hashed_password
        )
        self.session.add(admin)
        self.session.commit()

    def get_all_administrators(self):
        return self.session.query(Administration).all()

    def get_administration_by_id(self, admin_id):
        return self.session.query(Administration).get(admin_id)

    def get_administration_by_username(self, username: str) -> Administration:
        return self.session.query(Administration).filter(Administration.contact_info == username).first()

    def update_administration(self, admin_id, **kwargs):
        admin = self.get_administration_by_id(admin_id)
        if admin:
            for key, value in kwargs.items():
                setattr(admin, key, value)
            self.session.commit()

    def delete_administration(self, admin_id):
        admin = self.get_administration_by_id(admin_id)
        if admin:
            self.session.delete(admin)
            self.session.commit()