import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.2-1b-Instruct")
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")