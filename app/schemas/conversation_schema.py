from typing import Optional
from pydantic import BaseModel, Field
from uuid import uuid4, UUID

class ConversationSchema(BaseModel):
    uuid: UUID = Field(default_factory=uuid4, description="Identifier for the conversation")
    user_message: Optional[str] = Field(None, max_length=255, description="Message from user")
    chat_response: Optional[str] = Field(None, description="Response from chat")
 

    class Config:
        json_schema_extra = {
            "example": {
                "uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "user_message": "Summer Vacation",
                "chat_response": "We went to the beach...",
            }
        }