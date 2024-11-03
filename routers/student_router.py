from datetime import date
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager

router = APIRouter()
db_manager = get_db_manager()

class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    birth_date: str
    contact_info: str
    course: int
    is_non_local: bool
    password: str
    gender: str

class StudentResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    birth_date: date
    contact_info: str
    course: int
    is_non_local: bool
    gender: str

    class Config:
        from_attributes = True
        json_encoders = {
            date: lambda v: v.isoformat()
        }

@router.post("/", response_model=StudentResponse)
def create_student(student: StudentCreate):
    db_manager.students.add_student(**student.dict())
    new_student = db_manager.students.get_all_students()[-1]
    return new_student

@router.get("/", response_model=list[StudentResponse])
def read_students():
    return db_manager.students.get_all_students()