from datetime import date
from collections import defaultdict

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
    accommodations = db_manager.accommodations.get_all_accommodations()
    assigned_student_ids = {accommodation.student_id for accommodation in accommodations}
    new_accommodations = []

    # Update the available bed count in rooms
    for room in rooms:
        room.occupied_beds = len([accommodation for accommodation in room.accommodations if accommodation.date_to >= date.today()])
        db_manager.rooms.update_room(room.id, occupied_beds=room.occupied_beds)

    # Group students by group and gender
    grouped_students = defaultdict(list)
    for student_tuple in students_with_violations:
        student = student_tuple[0]
        if student.id not in assigned_student_ids:
            grouped_students[(student.grup, student.gender)].append(student)

    for (group, gender), students in grouped_students.items():
        for student in students:
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
                new_accommodations.append(accommodation)
                suitable_room.occupied_beds += 1
                db_manager.rooms.update_room(suitable_room.id, occupied_beds=suitable_room.occupied_beds)
            else:
                print(f"No suitable room found for student {student.id}")

    return new_accommodations