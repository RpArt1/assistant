from typing import Protocol, List, Dict
from ..domain.conversation import Conversation

class IConversationRepository(Protocol):
    async def get_conversation(self, uuid: str) -> list:
        """Fetch conversations by UUID and return formatted conversation history"""
        ...
    async def save_conversation(self, conversation: Conversation) -> None:
        """Save conversation to database"""
        ...
