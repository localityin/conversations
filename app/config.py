# app/config.py
import os
from dotenv import load_dotenv
from typing import List, Dict
import json

load_dotenv()  # Load variables from .env

class Settings:
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: int = int(os.getenv("REDIS_DB", 0))
    
    # Whitelisted intents for users
    WHITELISTED_USER_INTENTS: List[str] = json.loads(os.getenv("WHITELISTED_USER_INTENTS", "[]"))
    
    # Whitelisted intents for stores
    WHITELISTED_STORE_INTENTS: List[str] = json.loads(os.getenv("WHITELISTED_STORE_INTENTS", "[]"))
    
    # Mapping from intent to template name for users
    USER_INTENT_TEMPLATE_MAP: Dict[str, str] = json.loads(os.getenv("USER_INTENT_TEMPLATE_MAP", "{}"))
    
    # Mapping from intent to template name for stores
    STORE_INTENT_TEMPLATE_MAP: Dict[str, str] = json.loads(os.getenv("STORE_INTENT_TEMPLATE_MAP", "{}"))

settings = Settings()