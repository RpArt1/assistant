from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db_models import ConversationModel, ConversationMessageModel
from ..repositories.interfaces import IConversationRepository
from ..crud import conversation_crud
from ..domain.conversation import Conversation

# app/repositories/conversation_repository.py
class SQLAlchemyConversationRepository(IConversationRepository):

    def __init__(self, db: AsyncSession):
        self.db = db 

    async def get_conversation(self, id: str) -> Conversation: 
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
            return conversation            
        except Exception as e: 
            logging.error(f"Cannot fetch conversation with id {id}: {e}")

    async def save_conversation(self, conversation: Conversation) -> None:
        try:
            # todo convert messages to ConversationMessageModel 
            message_models = []
            for message in conversation.messages:
                message_model = ConversationMessageModel(
                    content = message.content,
                    role = message.role,
                    created_at = message.created_at
                )
                message_models.append(message_model)
            
            # todo convert messages to ConversationMessageModel 
            conversation_model = ConversationModel(
                id = conversation.id,
                title = conversation.title,
                status = conversation.status.value,
                meta_data = conversation.metadata,
                created_at = conversation.created_at,
                updated_at = conversation.updated_at, 
                messages = message_models
            )
            await conversation_crud.save_conversation(conversation_model, self.db)
        except Exception as e:
            logging.error(f"Cannot save conversation: {e}")