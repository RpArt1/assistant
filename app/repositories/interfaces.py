from typing import Protocol, List, Dict

class IConversationRepository(Protocol):
    async def fetch_conversation_by_uuid(self, uuid: str) -> list:
        """Fetch conversations by UUID and return formatted conversation history"""
        ...