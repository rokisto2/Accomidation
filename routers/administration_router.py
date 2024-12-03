from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager

router = APIRouter()
db_manager = get_db_manager()

class AdministrationCreate(BaseModel):
    first_name: str
    last_name: str
    contact_info: str
    dormitory_id: int
    password: str  # New field for password
    contributions: int = 0

class AdministrationResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    contact_info: str
    dormitory_id: int
    contributions: int

    class Config:
        from_attributes = True

@router.post("/", response_model=AdministrationResponse)
def create_administration(administration: AdministrationCreate):
    db_manager.administrations.add_administration(**administration.dict())
    return db_manager.administrations.get_all_administrators()[-1]

@router.get("/", response_model=list[AdministrationResponse])
def read_administrations():
    return db_manager.administrations.get_all_administrators()

@router.get("/{administration_id}", response_model=AdministrationResponse)
def read_administration(administration_id: int):
    administration = db_manager.administrations.get_administration_by_id(administration_id)
    if not administration:
        raise HTTPException(status_code=404, detail="Administration not found")
    return administration

@router.put("/{administration_id}", response_model=AdministrationResponse)
def update_administration(administration_id: int, administration: AdministrationCreate):
    db_manager.administrations.update_administration(administration_id, **administration.dict())
    return db_manager.administrations.get_administration_by_id(administration_id)

@router.delete("/{administration_id}", response_model=AdministrationResponse)
def delete_administration(administration_id: int):
    administration = db_manager.administrations.get_administration_by_id(administration_id)
    if not administration:
        raise HTTPException(status_code=404, detail="Administration not found")
    db_manager.administrations.delete_administration(administration_id)
    return administration