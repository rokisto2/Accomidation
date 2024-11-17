from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from db_manager_factory import get_db_manager

router = APIRouter()
db_manager = get_db_manager()

class FloorCreate(BaseModel):
    dormitory_id: int
    floor_number: int

class FloorResponse(BaseModel):
    id: int
    dormitory_id: int
    floor_number: int

    class Config:
        from_attributes = True

@router.post("/", response_model=FloorResponse)
def create_floor(floor: FloorCreate):
    db_manager.floors.add_floor(**floor.dict())
    return db_manager.floors.get_all_floors()[-1]

@router.get("/", response_model=list[FloorResponse])
def read_floors():
    return db_manager.floors.get_all_floors()

@router.get("/{floor_id}", response_model=FloorResponse)
def read_floor(floor_id: int):
    floor = db_manager.floors.get_floor_by_id(floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    return floor

@router.put("/{floor_id}", response_model=FloorResponse)
def update_floor(floor_id: int, floor: FloorCreate):
    db_manager.floors.update_floor(floor_id, **floor.dict())
    return db_manager.floors.get_floor_by_id(floor_id)

@router.delete("/{floor_id}", response_model=FloorResponse)
def delete_floor(floor_id: int):
    floor = db_manager.floors.get_floor_by_id(floor_id)
    if not floor:
        raise HTTPException(status_code=404, detail="Floor not found")
    db_manager.floors.delete_floor(floor_id)
    return floor