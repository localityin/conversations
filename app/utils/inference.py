import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from app.config import Config
from app.utils.logger import log_message
from app.constants.system_prompts import USER_SYSTEM_PROMPT, user_known_intents

device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME, use_auth_token=Config.HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(Config.MODEL_NAME, use_auth_token=Config.HUGGINGFACE_TOKEN)
model.to(device)

def filter_user_intent(message: str) -> str:
    for intent in user_known_intents:
        if intent in message:
            return intent
    return 'user_unknown_message'

def filter_store_intent(message: str) -> str:
    return 'store_unknown_message'

def get_user_intent(messages: list) -> str:
    # Refine context construction
    context = USER_SYSTEM_PROMPT + f"\nUser: {messages[0]}\nResponse: "
    log_message("info", f"User message: {messages[0]}")
    log_message("debug", f"Context passed to model: {context}")
    
    # Tokenize and generate response
    inputs = tokenizer(context, return_tensors="pt").to(device)
    outputs = model.generate(
        **inputs,
        max_length=700,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id
    )

    # Decode the response and clean up the output
    response = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    log_message("debug", f"Model generated response: {response}")

    # Extract and filter the intent
    intent = response.split("\n")[-1].strip()  # Take the last line
    intent = filter_user_intent(intent)  # Validate against known intents

    log_message("info", f"Extracted intent: {intent}")
    return intent

def get_store_intent(messages: list) -> str:
    intent = filter_store_intent(messages[0])
    return intent