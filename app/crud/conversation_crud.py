from sqlalchemy.ext.asyncio import AsyncSession
import logging

from ..schemas.conversation_schema import ConversationSchema
from ..models.db_models import Conversation


async def save_conversation(conversation: ConversationSchema, db: AsyncSession) -> Conversation:
    try:
        db_memory = Conversation(
            uuid=conversation.uuid,
            user_message=conversation.user_message,
            chat_response=conversation.chat_response,
        )
        db.add(db_memory)
        await db.commit()
        await db.refresh(db_memory)

        return db_memory
    
    except Exception as e: 
        logging.error(e)
