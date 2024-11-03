from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager

router = APIRouter()
db_manager = get_db_manager()

class DeaneryStaffCreate(BaseModel):
    first_name: str
    last_name: str
    contact_info: str
    password: str

class DeaneryStaffResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact_info: str

    class Config:
        from_attributes = True

@router.post("/", response_model=DeaneryStaffResponse)
def create_deanery_staff(staff: DeaneryStaffCreate):
    db_manager.deanery_staff.add_deanery_staff(**staff.dict())
    new_staff = db_manager.deanery_staff.get_all_deanery_staff()[-1]
    return new_staff


@router.get("/", response_model=list[DeaneryStaffResponse])
def read_deanery_staff():
    return db_manager.deanery_staff.get_all_deanery_staff()