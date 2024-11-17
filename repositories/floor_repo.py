from models import Floor

class FloorRepository:
    def __init__(self, session):
        self.session = session

    def add_floor(self, dormitory_id, floor_number):
        floor = Floor(dormitory_id=dormitory_id, floor_number=floor_number)
        self.session.add(floor)
        self.session.commit()

    def get_all_floors(self):
        return self.session.query(Floor).all()

    def get_floor_by_id(self, floor_id):
        return self.session.query(Floor).get(floor_id)

    def update_floor(self, floor_id, **kwargs):
        floor = self.get_floor_by_id(floor_id)
        if floor:
            for key, value in kwargs.items():
                setattr(floor, key, value)
            self.session.commit()

    def delete_floor(self, floor_id):
        floor = self.get_floor_by_id(floor_id)
        if floor:
            self.session.delete(floor)
            self.session.commit()