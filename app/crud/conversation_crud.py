from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import asc
import logging

from ..models.db_models import ConversationModel


async def fetch_conversation_by_id(id: str, db: AsyncSession) -> ConversationModel:
    try: 
        result = await db.execute(
            select(ConversationModel)
            .where(ConversationModel.id == id )
        )
        conversation = result.scalar_one_or_none()
        return conversation 
    except Exception as e:
        logging.error(f"Error fetching conversation with id {id}: {e}")
        return None