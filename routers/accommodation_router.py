from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager
from datetime import date

from algoritms import distributeStudents


router = APIRouter()

db_manager = get_db_manager()

class AccommodationCreate(BaseModel):
    student_id: int
    room_id: int
    date_from: date

class AccommodationResponse(BaseModel):
    student_id: int
    room_id: int
    date_from: date

    class Config:
        from_attributes = True

@router.post("/", response_model=AccommodationResponse)
def create_accommodation(accommodation: AccommodationCreate):
    db_manager.accommodations.add_accommodation(**accommodation.dict())
    return db_manager.accommodations.get_all_accommodations()[-1]

@router.get("/", response_model=list[AccommodationResponse])
def read_accommodations():
    return db_manager.accommodations.get_all_accommodations()

@router.get("/{accommodation_id}", response_model=AccommodationResponse)
def read_accommodation(accommodation_id: int):
    accommodation = db_manager.accommodations.get_accommodation_by_id(accommodation_id)
    if not accommodation:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    return accommodation

@router.put("/{accommodation_id}", response_model=AccommodationResponse)
def update_accommodation(accommodation_id: int, accommodation: AccommodationCreate):
    db_manager.accommodations.update_accommodation(accommodation_id, **accommodation.dict())
    return db_manager.accommodations.get_accommodation_by_id(accommodation_id)

@router.delete("/{accommodation_id}", response_model=AccommodationResponse)
def delete_accommodation(accommodation_id: int):
    accommodation = db_manager.accommodations.get_accommodation_by_id(accommodation_id)
    if not accommodation:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    db_manager.accommodations.delete_accommodation(accommodation_id)
    return accommodation

@router.get("/by_dormitory/{dormitory_id}")
async def read_accommodations_by_dormitory(dormitory_id: int):
    # Replace with actual database query
    accommodations = db_manager.accommodations.get_accommodations_by_dormitory_id(dormitory_id)
    return accommodations

@router.get("/by_student/{student_id}", response_model=AccommodationResponse)
async def read_accommodations_by_student(student_id: int):
    # Replace with actual database query
    accommodations = db_manager.accommodations.get_accommodations_by_student_id(student_id)
    if not accommodations:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    else:
        return accommodations



@router.post("/distribute", response_model=list[AccommodationResponse])
def distribute_students():
    accommodations = distributeStudents.distribute_students(db_manager)
    return accommodations


@router.delete("/evict/{student_id}", response_model=AccommodationResponse)
def evict_student(student_id: int):
    accommodation = db_manager.accommodations.get_accommodations_by_student_id(student_id)
    if not accommodation:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    # Update the room's occupied beds count
    room = db_manager.rooms.get_room_by_id(accommodation.room_id)
    if room:
        room.occupied_beds -= 1
        db_manager.rooms.update_room(room.id, occupied_beds=room.occupied_beds)

    db_manager.accommodations.delete_accommodation(accommodation.id)
    return accommodation

@router.delete("/evict_all/", response_model=AccommodationResponse)
def evict_student():
    accommodations1 = db_manager.accommodations.get_all_accommodations()
    if not accommodations1:
        raise HTTPException(status_code=404, detail="Accommodation not found")

    # Update the room's occupied beds count
    for accommodation in accommodations1:

        room = db_manager.rooms.get_room_by_id(accommodation.room_id)
        if room:
            room.occupied_beds -= 1
            db_manager.rooms.update_room(room.id, occupied_beds=room.occupied_beds)

        db_manager.accommodations.delete_accommodation(accommodation.id)

    return accommodations1

