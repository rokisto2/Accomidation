from models import Dormitory

class DormitoryRepository:
    def __init__(self, session):
        self.session = session

    def add_dormitory(self, name, address, description):
        dormitory = Dormitory(name=name, address=address, description=description)
        self.session.add(dormitory)
        self.session.commit()

    def get_all_dormitories(self):
        return self.session.query(Dormitory).all()

    def get_dormitory_by_id(self, dormitory_id):
        return self.session.query(Dormitory).get(dormitory_id)

    def update_dormitory(self, dormitory_id, **kwargs):
        dormitory = self.get_dormitory_by_id(dormitory_id)
        if dormitory:
            for key, value in kwargs.items():
                setattr(dormitory, key, value)
            self.session.commit()

    def delete_dormitory(self, dormitory_id):
        dormitory = self.get_dormitory_by_id(dormitory_id)
        if dormitory:
            self.session.delete(dormitory)
            self.session.commit()
