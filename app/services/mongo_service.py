from pymongo import MongoClient
from app.config import Config

class MongoService:
    def __init__(self):
        self.client = MongoClient(Config.MONGO_URI)
        self.db = self.client["locality"]
        self.collection = self.db["messages"]

    async def load_to_redis(self, redis_service):
        for user_data in self.collection.find():
            user_id = user_data["_id"]
            messages = user_data.get("messages", [])
            redis_service.client.ltrim(user_id, 1, 0)
            redis_service.client.rpush(user_id, *messages[-10:])

    async def backup_from_redis(self, redis_service):
        for key in redis_service.client.scan_iter():
            messages = redis_service.client.lrange(key, 0, -1)
            self.collection.update_one({"_id": key}, {"$set": {"messages": messages}}, upsert=True)