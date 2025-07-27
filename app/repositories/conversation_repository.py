from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.conversation_schema import ConversationSchema
from ..repositories.interfaces import IConversationRepository
from ..crud import conversation_crud

# app/repositories/conversation_repository.py
class SQLAlchemyConversationRepository(IConversationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db 

    async def fetch_conversations_by_uuid(self, uuid: str) -> list: 
        """fetch convresations based on uuid of converasation
        Args:
            uuid (str): _description_
        Returns:
            list: json list of conversations or empty list 
        """

        try: 
            conversation_list = await conversation_crud.fetch_conversations_by_uuid(uuid, self.db)
            conversations = conversation_list.scalars().all()
            json_conversation_list = []
            for conversation in conversations:
                json_conversation_list.append({"role": "user", "content": conversation.user_message})
                json_conversation_list.append({"role": "assistant", "content": conversation.chat_response})
            return json_conversation_list

        except Exception as e: 
            logging.error(f"Cannot sava conversation: {e}")

    async def save_conversation(self, conversation: ConversationSchema):
        await conversation_crud.save_conversation(conversation, self.db)
