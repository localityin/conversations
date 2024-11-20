from pydantic import BaseModel, Field, field_validator

class InferenceRequest(BaseModel):
    user_id: str
    message: str
    fast: bool = False

class InferenceRequestV2(BaseModel):
    phone: int = Field(..., example=9987130333)
    message: str = Field(..., example="I want to open an account")
    isStore: bool = Field(..., example=True)

    @field_validator('phone')
    def phone_must_be_valid(cls, v):
        if not (1000000000 <= v <= 9999999999):
            raise ValueError('Phone number must be a 10-digit integer')
        return v
    
class InferenceResponseV2(BaseModel):
    intent: str
    template_name: str
