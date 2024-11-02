# app/utils.py
import redis
from typing import List, Tuple
from app.config import settings

class RedisClient:
    def __init__(self):
        self.client = redis.Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            db=settings.REDIS_DB,
            decode_responses=True
        )
    
    def add_message(self, phone: int, message: str, message_type: str = "User"):
        key = f"messages:{phone}"
        # Store messages as "Type: Message" for clarity
        formatted_message = f"{message_type}: {message}"
        self.client.rpush(key, formatted_message)
    
    def get_messages(self, phone: int) -> List[str]:
        key = f"messages:{phone}"
        return self.client.lrange(key, 0, -1)

redis_client = RedisClient()