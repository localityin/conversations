import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers import pipeline
from app.config import Config
from app.utils.logger import log_message
from app.constants.system_prompts import USER_SYSTEM_PROMPT, STORE_SYSTEM_PROMPT, user_known_intents, store_known_intents, store_intent_descriptions, user_intent_descriptions

log_message("info", "Loading model and tokenizer...")
device = "cuda" if torch.cuda.is_available() else "cpu"
tokenizer = AutoTokenizer.from_pretrained(Config.MODEL_NAME, token=Config.HUGGINGFACE_TOKEN)
model = AutoModelForCausalLM.from_pretrained(Config.MODEL_NAME, token=Config.HUGGINGFACE_TOKEN)
model.to(device)
log_message("info", "Model and tokenizer loaded successfully")

def filter_intent(is_store, message: str) -> str:
    intents = store_known_intents if is_store else user_known_intents
    for intent in intents:
        if intent in message:
            return intent
    return 'user_unknown_message' if not is_store else 'store_unknown_message'

def get_intent(is_store, messages: list) -> str:
    # Refine context construction
    actor = 'Store' if is_store else 'User'
    prompt = STORE_SYSTEM_PROMPT if is_store else USER_SYSTEM_PROMPT

    context = prompt + f"\n{actor}: {messages[0]}\nResponse: "
    log_message("info", f"{actor} message: {messages[0]}")
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
    intent = filter_intent(is_store, intent)  # Validate against known intents

    log_message("info", f"Extracted intent: {intent}")
    return intent

classifier = pipeline("zero-shot-classification", model=Config.SMALL_MODEL_NAME, device=0)

def faster_get_intent(is_store, messages: list) -> str:
    message = messages[0]
    intents = store_known_intents if is_store else user_known_intents

    intent_descriptions = store_intent_descriptions if is_store else user_intent_descriptions

    # Prepare candidate labels
    candidate_labels = [intent_descriptions[intent] for intent in intents]

    # Perform classification
    result = classifier(message, candidate_labels)

    # Get the top label and map back to the intent identifier
    top_label = result['labels'][0]
    description_to_intent = {v: k for k, v in intent_descriptions.items()}
    intent = description_to_intent[top_label]

    log_message("info", f"Extracted intent: {intent}")
    return intent