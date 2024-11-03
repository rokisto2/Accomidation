from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from repositories import StudentRepository
from repositories import DormitoryRepository
from repositories import RoomRepository
from repositories import ViolationRepository
from repositories import AdministrationRepository
from repositories import AccommodationRepository
from repositories import DeaneryStaffRepository

class DBManager:
    def __init__(self, user, password, host, port, db_name):
        db_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}"
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine, )
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Подключение репозиториев
        self.students = StudentRepository(self.session)
        self.dormitories = DormitoryRepository(self.session)
        self.rooms = RoomRepository(self.session)
        self.violations = ViolationRepository(self.session)
        self.administrations = AdministrationRepository(self.session)
        self.accommodations = AccommodationRepository(self.session)
        self.deanery_staff = DeaneryStaffRepository(self.session)

    def close(self):
        self.session.close()
