from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class MemoryCreate(BaseModel):
    uuid: uuid4 = Field(..., description="Unique identifier for the memory")
    name: Optional[str] = Field(None, max_length=255, description="Name of the memory")
    content: Optional[str] = Field(None, description="Content of the memory")
    reflection: Optional[str] = Field(None, description="Personal reflection on the memory")
    tags: Optional[List[str]] = Field(default=[], description="List of tags associated with the memory")
    active: bool = Field(default=True, description="Whether the memory is active or not")
    source: Optional[str] = Field(None, max_length=255, description="Source of the memory")

    class Config:
        schema_extra = {
            "example": {
                "uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "name": "Summer Vacation",
                "content": "We went to the beach...",
                "reflection": "It was a great day...",
                "tags": ["vacation", "beach", "summer"],
                "active": True,
                "source": "personal"
            }
        }


class MemoryResponse(BaseModel):
    id: int = Field(..., description="Database ID of the memory")
    uuid: str = Field(..., description="Unique identifier for the memory")
    name: Optional[str] = Field(None, max_length=255, description="Name of the memory")
    content: Optional[str] = Field(None, description="Content of the memory")
    reflection: Optional[str] = Field(None, description="Personal reflection on the memory")
    tags: List[str] = Field(default=[], description="List of tags associated with the memory")
    active: bool = Field(..., description="Whether the memory is active or not")
    source: Optional[str] = Field(None, max_length=255, description="Source of the memory")
    created_at: datetime = Field(..., description="The date and time the memory was created")

    class Config:
        orm_mode = True

        schema_extra = {
            "example": {
                "id": 1,
                "uuid": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
                "name": "Summer Vacation",
                "content": "We went to the beach...",
                "reflection": "It was a great day...",
                "tags": ["vacation", "beach", "summer"],
                "active": True,
                "source": "personal",
                "created_at": "2024-03-11T12:34:56"
            }
        }
