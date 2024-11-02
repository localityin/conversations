# app/schemas.py
from pydantic import BaseModel, Field, field_validator

class InferenceRequest(BaseModel):
    phone: int = Field(..., example=9987130333)
    message: str = Field(..., example="I want to open an account")
    isStore: bool = Field(..., example=True)

    @field_validator('phone')
    def phone_must_be_valid(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be a 10-digit integer')
        return v
    
class InferenceResponse(BaseModel):
    intent: str
    template_name: str
