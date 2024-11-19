from models import Room

class RoomRepository:
    def __init__(self, session):
        self.session = session

    def add_room(self, floor_id, room_number, room_type, bed_count):
        room = Room(floor_id=floor_id, room_number=room_number, room_type=room_type, bed_count=bed_count)
        self.session.add(room)
        self.session.commit()

    def get_all_rooms(self):
        return self.session.query(Room).all()

    def get_room_by_id(self, room_id):
        return self.session.query(Room).get(room_id)

    def update_room(self, room_id, **kwargs):
        room = self.get_room_by_id(room_id)
        if room:
            for key, value in kwargs.items():
                setattr(room, key, value)
            self.session.commit()

    def delete_room(self, room_id):
        room = self.get_room_by_id(room_id)
        if room:
            self.session.delete(room)
            self.session.commit()

    def get_rooms_by_floor_id(self, floor_id: int):
        return self.session.query(Room).filter_by(floor_id=floor_id).all()