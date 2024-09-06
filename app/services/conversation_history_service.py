from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends

from ..utils import file_processor
from . import open_ai_service
from ..crud import conversation_crud
from ..dependencies import get_db_session
from ..schemas.conversation_schema import ConversationSchema


async def fetch_conversations_by_uuid(uuid: str, db ) -> tuple: 
    try: 
        conversation_list = await conversation_crud.fetch_conversations_by_uuid(uuid, db)
        conversations = conversation_list.scalars().all()
        json_conversation_list = []
        for conversation in conversations:
            json_conversation_list.append({"role": "user", "content": conversation.user_message})
            json_conversation_list.append({"role": "assistant", "content": conversation.chat_response})
        return json_conversation_list

    except Exception as e: 
        logging.error(f"Cannot sava conversation: {e}")
