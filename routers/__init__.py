from .student_router import router as student_router
from .dormitory_router import router as dormitory_router
from .room_router import router as room_router
from .violation_router import router as violation_router
from .administration_router import router as administration_router
from .accommodation_router import router as accommodation_router
from .auth_router import router as auth_router
from .deanery_staff_router import router as deanery_staff_router
# Массив, содержащий кортежи (роутер, название)
routers = [
    (student_router, "students"),
    (dormitory_router, "dormitories"),
    (room_router, "rooms"),
    (violation_router, "violations"),
    (administration_router, "administration"),
    (accommodation_router, "accommodations"),
    (auth_router, "auth"),
    (deanery_staff_router, "deanery_staff")
]
