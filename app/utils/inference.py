from ctransformers import AutoModelForCausalLM
from app.config import Config
from app.utils.logger import log_message
from app.constants.system_prompts import USER_SYSTEM_PROMPT, STORE_SYSTEM_PROMPT, user_known_intents, store_known_intents

log_message("info", "Loading model...")
model = AutoModelForCausalLM.from_pretrained(Config.MODEL_PATH, model_type="llama")
log_message("info", "Model loaded successfully")

def filter_intent(is_store, message: str) -> str:
    intents = store_known_intents if is_store else user_known_intents
    for intent in intents:
        if intent in message:
            return intent
    return 'user_unknown_message' if not is_store else 'store_unknown_message'

def get_intent(is_store, messages: list) -> str:
    actor = 'Store' if is_store else 'User'
    prompt = STORE_SYSTEM_PROMPT if is_store else USER_SYSTEM_PROMPT

    context = f"{prompt}\n{actor}: {messages[0]}\nResponse:"
    log_message("info", f"{actor} message: {messages[0]}")
    log_message("debug", f"Context passed to model: {context}")
    
    # Generate response
    response = model(context, max_new_tokens=700, temperature=0.7)  # Adjust temperature as needed
    response = response.strip()
    log_message("debug", f"Model generated response: {response}")

    # Extract and filter the intent
    intent = response.split("\n")[-1].strip()  # Take the last line
    intent = filter_intent(is_store, intent)  # Validate against known intents

    log_message("info", f"Extracted intent: {intent}")
    return intent