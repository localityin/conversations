from fastapi import FastAPI
from app.models import InferenceRequest
from app.services.mongo_service import MongoService
from app.services.redis_service import RedisService
# from app.utils.inference import get_intent, faster_get_intent
from app.services.openai_service import OpenAIService
from app.utils.logger import log_message

app = FastAPI()

mongo_service = MongoService()
redis_service = RedisService()
openai_service = OpenAIService()

@app.on_event("startup")
async def startup_event():
    await mongo_service.load_to_redis(redis_service)

@app.on_event("shutdown")
async def shutdown_event():
    await mongo_service.backup_from_redis(redis_service)

@app.post("/inference/user")
async def inference(request: InferenceRequest):
    user_id, message, fast = request.user_id, request.message, request.fast
    log_message("info", f"Received message from user {user_id}: {message}. Fast: {fast}")

    # Retrieve the last 10 messages for context
    redis_service.add_message(user_id, message)

    # Perform inference
    intent = openai_service.get_intent(message, False)

    return {"intent": intent}

@app.post("/inference/store")
async def inference(request: InferenceRequest):
    user_id, message, fast = request.user_id, request.message, request.fast
    log_message("info", f"Received message from store {user_id}: {message}. Fast: {fast}")

    # Retrieve the last 10 messages for context
    redis_service.add_message(user_id, message)

    # Perform inference
    intent = openai_service.get_intent(message, True)

    return {"intent": intent}