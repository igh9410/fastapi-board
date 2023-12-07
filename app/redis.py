import redis
from app.config import Settings

redis_client = redis.Redis.from_url(Settings.REDIS_URL)