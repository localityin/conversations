import redis
from app.config import Config
from app.utils.logger import log_message

class RedisService:
    def __init__(self):
        self.client = redis.Redis(
            host=Config.REDIS_HOST, 
            port=Config.REDIS_PORT,
            username=Config.REDIS_USER,
            password=Config.REDIS_PASSWORD,
            decode_responses=True
        )
        log_message("info", "Redis connection established")

    def add_message(self, user_id: str, message: str) -> list:
        if len(self.client.lrange(user_id, 0, -1)) >= 10:
            self.client.lpop(user_id)
        self.client.rpush(user_id, message)
        return self.client.lrange(user_id, 0, -1)