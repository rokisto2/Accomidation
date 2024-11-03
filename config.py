class Settings:
    DB_USER = "root"
    DB_PASSWORD = "1111"
    DB_HOST = "localhost"
    DB_PORT = 3306
    DB_NAME = "dormitory_management"

    @property
    def db_url(self):
        return f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
