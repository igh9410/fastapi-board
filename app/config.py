import os

from fastapi.security import HTTPBearer

class Settings:
   DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://developer:devpassword@localhost:25000/developer")
   REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:25100")
   # Configuration
   SECRET_KEY = os.getenv("JWT_SECRET_KEY", "UYaGFRTeAJ_q5psBZMwBNJhWVKmDYn3I4SicIxk7D_8=")
   SESSION_SECRET_KEY = os.getenv("SESSION_SECRET_KEY", "IdwJ9b6B9gBitU8HQc3-Lv5eN9XbC40qmdtmps7xDRY=")
   ALGORITHM = "HS256"
   ACCESS_TOKEN_EXPIRE_MINUTES = 30
   SECURITY = HTTPBearer()


settings = Settings()
