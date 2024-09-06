from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc
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

async def fetch_conversations_by_uuid(uuid: str, db: AsyncSession) -> list[Conversation]:
    try:
        conversations = await db.execute(select(Conversation).where(Conversation.uuid == uuid).order_by(asc(Conversation.created_at)))
        return conversations
    except Exception as e:
        logging.error(f"Error fetching conversations with uuid {uuid}: {e}")
        return []