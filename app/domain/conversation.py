# app/domain/conversation.py

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Dict, Any
from sqlalchemy.engine import create
from enum import Enum
from uuid import uuid4

class MessageRole:
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class ConversationStatus(Enum):
    ACTIVE = "active"
    CLOSED = "closed"
    ARCHIVED = "archived"


@dataclass
class Message:
    id: Optional[int] = None
    role: MessageRole = MessageRole.USER
    content: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self.role.value,
            "content": self.content,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat()
        }


@dataclass
class Conversation:
    """Aggregate root for conversation domain"""
    id: str = field(default_factory=lambda: str(uuid4()))
    title: Optional[str] = None
    status: ConversationStatus = ConversationStatus.ACTIVE
    metadata: Dict[str, Any] = field(default_factory=dict)
    messages: List[Message] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    
    def add_message(self, role: MessageRole, content: str, metadata: Dict[str, Any] = None) -> Message:
        """Add a message to the conversation"""
        message = Message(
            role=role,
            content=content,
            metadata=metadata or {}
        )
        self.messages.append(message)
        self.updated_at = datetime.now()
        return message