import os

class Settings:
   DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://developer:devpassword@localhost:25000/developer")

settings = Settings()
