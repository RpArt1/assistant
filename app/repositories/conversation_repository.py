from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..repositories.interfaces import IConversationRepository
from ..crud import conversation_crud
from ..domain.conversation import Conversation

# app/repositories/conversation_repository.py
class SQLAlchemyConversationRepository(IConversationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db 

    async def fetch_conversations_by_uuid(self, id: str) -> list: 
        try: 
            conversation_model = await conversation_crud.fetch_conversation_by_id(id, self.db)
            if not conversation_model:
                logging.info(f"No conversation found with id {id}")
                return None

            conversation = Conversation(
                id=conversation_model.id,
                title=conversation_model.title,
                status=conversation_model.status,
                metadata=conversation_model.meta_data,
            )
            
        except Exception as e: 
            logging.error(f"Cannot fetch conversation with id {id}: {e}")