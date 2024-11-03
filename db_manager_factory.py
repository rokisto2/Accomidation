from db_manager import DBManager
from config import settings

def get_db_manager():
    return DBManager(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        db_name=settings.DB_NAME
    )
