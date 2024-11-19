from models import Accommodation, Room, Floor
from datetime import datetime, timedelta


class AccommodationRepository:
    def __init__(self, session):
        self.session = session

    def add_accommodation(self, student_id, room_id, date_from = datetime.today(), date_to=datetime.today()+timedelta(days=365)):
        accommodation = Accommodation(student_id=student_id, room_id=room_id, date_from=date_from, date_to=date_to)
        self.session.add(accommodation)
        self.session.commit()

    def get_all_accommodations(self):
        return self.session.query(Accommodation).all()

    def get_accommodation_by_id(self, accommodation_id):
        return self.session.query(Accommodation).get(accommodation_id)

    def update_accommodation(self, accommodation_id, **kwargs):
        accommodation = self.get_accommodation_by_id(accommodation_id)
        if accommodation:
            for key, value in kwargs.items():
                setattr(accommodation, key, value)
            self.session.commit()

    def delete_accommodation(self, accommodation_id):
        accommodation = self.get_accommodation_by_id(accommodation_id)
        if accommodation:
            self.session.delete(accommodation)
            self.session.commit()

    def get_accommodations_by_student_id(self, student_id):
        return self.session.query(Accommodation).filter(Accommodation.student_id == student_id).first()

    def get_accommodations_by_dormitory_id(self, dormitory_id):
        return self.session.query(Accommodation).join(Room).join(Floor).filter(Floor.dormitory_id == dormitory_id).all()