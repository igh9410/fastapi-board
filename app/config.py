import os

class Settings:
   DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://developer:devpassword@localhost:25000/developer")
   REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:25100")

settings = Settings()
