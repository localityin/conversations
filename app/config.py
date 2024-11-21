import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    PORT = int(os.getenv("PORT", 8001))
    
    MONGO_URI = os.getenv("MONGO_URI")
    MONGO_DB = os.getenv("MONGO_DB")
    
    REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    REDIS_USER = os.getenv("REDIS_USER", "")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "")

    MODEL_NAME = os.getenv("MODEL_NAME", "meta-llama/Llama-3.2-1b-Instruct")
    MODEL_PATH = os.getenv("MODEL_PATH", "app/models/Llama-3.2-1B-Instruct-Q4_K_M.gguf")
    
    HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN", "")

    OPENAI_MODEL_NAME = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")