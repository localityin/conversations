import openai
from app.config import Config
from app.constants.system_prompts import USER_SYSTEM_PROMPT, STORE_SYSTEM_PROMPT, store_known_intents, user_known_intents
from app.utils.logger import log_message

class OpenAIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.store_system_prompt = STORE_SYSTEM_PROMPT
        self.user_system_prompt = USER_SYSTEM_PROMPT
        self.cached_prompts = {
            "user": {"role": "system", "content": self.user_system_prompt.strip()},
            "store": {"role": "system", "content": self.store_system_prompt.strip()},
        }
        log_message("info", "OpenAI service initialized")

    def filter_intent(self, is_store, message: str) -> str:
        intents = store_known_intents if is_store else user_known_intents
        for intent in intents:
            if intent in message:
                return intent
        return 'user_unknown_message' if not is_store else 'store_unknown_message'

    def get_intent(self, message: str, is_store: bool) -> str:
        """
        Detects intent from a user or store message.

        Args:
            message (str): The message from the user or store.
            is_store (bool): Whether the message is from a store. If False, assumes the message is from a user.

        Returns:
            str: The intent identifier as per the system prompts.
        """
        system_prompt = self.cached_prompts["store"] if is_store else self.cached_prompts["user"]
        try:
            response = openai.chat.completions.create(
                model=Config.OPENAI_MODEL_NAME,
                messages=[
                    system_prompt,
                    {"role": "user", "content": message}
                ],
                max_tokens=600,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "text"
                }
            )
            log_message("info", f"OpenAI response: {response}")
            intent = response.choices[0].message.content.strip()
            intent = self.filter_intent(is_store, intent)
            intent = self.filter_intent(is_store, intent)
            log_message("info", f"Filtered intent: {intent}")
            return intent
        except Exception as e:
            # Log the exception or handle it as per your application's need
            log_message("error", f"Error: {e}")
            return 'user_unknown_message' if not is_store else 'store_unknown_message'
        
openai_service = OpenAIService()