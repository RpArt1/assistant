# app/domain/conversation.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from sqlalchemy.engine import create

class MessageRole:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

@dataclass
class Message:
    role: MessageRole
    content: str
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class Conversation:
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_message (self, role: MessageRole, content:str) -> None:
        message = Message(role=role, content=content)
        self.messages.append(message)
        self.updated_at = datetime.now()
    
    def get_recent_messages(self, limit: int = 10) ->List[Message]