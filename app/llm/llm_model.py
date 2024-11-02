# app/llm/llm_model.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from app.config import settings
import os

class LLMModel:
    def __init__(self):
        model_name = "meta-llama/LLaMA-3.2-1B-Instruct"  # Replace with actual model path/name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto"
        )
        # Intents
        self.whitelisted_user_intents = settings.WHITELISTED_USER_INTENTS
        self.whitelisted_store_intents = settings.WHITELISTED_STORE_INTENTS
        # Intent to Template Mapping
        self.user_intent_template_map = settings.USER_INTENT_TEMPLATE_MAP
        self.store_intent_template_map = settings.STORE_INTENT_TEMPLATE_MAP

    def predict_intent(self, context_messages: list, latest_message: str, is_store: bool) -> tuple[str, str]:
        prompt = self.construct_prompt(context_messages, latest_message, is_store)
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad():
            outputs = self.model.generate(**inputs, max_length=150)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        intent = self.parse_intent(response)
        
        # Select appropriate whitelist and template map
        if is_store:
            if intent not in self.whitelisted_store_intents:
                intent = "store_unknown_message"
            template_name = self.store_intent_template_map.get(intent, "store_unknown_message")
        else:
            if intent not in self.whitelisted_user_intents:
                intent = "user_unknown_message"
            template_name = self.user_intent_template_map.get(intent, "user_unknown_message")
        
        return intent, template_name

    def construct_prompt(self, context_messages: list, latest_message: str, is_store: bool) -> str:
        # Define the preset instructions based on the message type
        if is_store:
            preset = (
                "You are an intelligent assistant that helps classify store messages into predefined intents. "
                f"The allowed intents are: {', '.join(self.whitelisted_store_intents)}. "
                "If the store's intent does not match any of these, respond with 'store_unknown_message'.\n\n"
                "Conversation History:\n"
            )
        else:
            preset = (
                "You are an intelligent assistant that helps classify user messages into predefined intents. "
                f"The allowed intents are: {', '.join(self.whitelisted_user_intents)}. "
                "If the user's intent does not match any of these, respond with 'user_unknown_message'.\n\n"
                "Conversation History:\n"
            )
        
        # Append previous messages
        for msg in context_messages:
            preset += f"User: {msg}\n" if not is_store else f"Store: {msg}\n"
        
        # Append latest message
        preset += f"User: {latest_message}\n" if not is_store else f"Store: {latest_message}\n"
        
        # Intent prompt
        preset += "Intent:"
        return preset

    def parse_intent(self, response: str) -> str:
        # Extract the first word in the response as the intent
        return response.strip().split()[0].lower()

llm_model = LLMModel()
