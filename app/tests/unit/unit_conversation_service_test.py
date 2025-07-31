import pytest
from unittest.mock import patch, Mock


#from app.services.conversation_service import ConversationService


class MockConversationRepository:
    async def fetch_conversations_by_uuid(self, uuid: str) -> list: 
        conversations = [
            {"role": "user", "content": "test message 1"},
            {"role": "assistant", "content": "test response 1"},
            {"role": "user", "content": "test message 2"}, 
            {"role": "assistant", "content": "test response 2"}
        ]
        return conversations


# class UnitConversationServiceTest: 
#     @pytest.mark.skip(reason="Temporarily disabled")
#     def reply_user_test(self):
#         mock_conversations_repository = MockConversationRepository()
#         conversation_service = ConversationService(mock_conversations_repository)
#         conversation_service.reply_user(1112)
