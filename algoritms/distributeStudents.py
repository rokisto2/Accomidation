from datetime import date

from sqlalchemy.orm import Session
from sqlalchemy import join
from sqlalchemy import func

from db_manager import DBManager
from models import Violation
from models.student import Student, GenderEnum
from models.room import Room, RoomTypeEnum
from models.accommodation import Accommodation
from repositories import StudentRepository

def distribute_students(db_manager: DBManager):
    students_with_violations = db_manager.students.get_sorted_students()
    rooms = db_manager.rooms.get_all_rooms()
    accommodations = []

    for student_tuple in students_with_violations:
        student = student_tuple[0]
        suitable_room = None
        for room in rooms:
            if room.room_type == RoomTypeEnum.male and student.gender == GenderEnum.male and room.occupied_beds < room.bed_count:
                suitable_room = room
                break
            elif room.room_type == RoomTypeEnum.female and student.gender == GenderEnum.female and room.occupied_beds < room.bed_count:
                suitable_room = room
                break

        if suitable_room:
            accommodation = Accommodation(student_id=student.id, room_id=suitable_room.id, date_from=date.today())
            db_manager.accommodations.add_accommodation(student_id=student.id, room_id=suitable_room.id)
            accommodations.append(accommodation)
            suitable_room.occupied_beds += 1
        else:
            print(f"No suitable room found for student {student.id}")

    return accommodations