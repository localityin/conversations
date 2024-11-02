# app/main.py
from fastapi import FastAPI, HTTPException
from app.schemas import InferenceRequest, InferenceResponse
from app.utils import redis_client
from app.llm.llm_model import llm_model
import uvicorn
import logging
import redis

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="Inference API", version="1.1")

@app.post("/inference", response_model=InferenceResponse)
def inference_endpoint(request: InferenceRequest):
    try:
        logger.info(f"Received message from {'Store' if request.isStore else 'User'}: {request.message}")

        # Store the incoming message with additional context if needed
        message_type = "Store" if request.isStore else "User"
        redis_client.add_message(request.phone, request.message, message_type)
        
        # Fetch all previous messages for context
        messages = redis_client.get_messages(request.phone)
        
        # Predict intent and get template name using LLM
        intent, template_name = llm_model.predict_intent(messages[:-1], messages[-1], request.isStore)
        
        return InferenceResponse(intent=intent, template_name=template_name)
    except redis.RedisError as re:
        logger.error(f"Redis error: {re}")
        raise HTTPException(status_code=503, detail="Service Unavailable: Redis Error")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

# Optional: For running directly with `python main.py`
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
