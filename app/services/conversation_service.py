from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends

from ..utils import file_processor
from ..services import open_ai_service
from ..crud import conversation_crud
from ..dependencies import get_db_session
from ..schemas.conversation_schema import ConversationSchema


async def reply_user(user_message:str, conversation_id:str, db: AsyncSession = Depends(get_db_session)) -> str:
    try: 
        logging.info(f"{conversation_id} ==> User posted message: {user_message}")
        current_date = (datetime.now()).strftime("%Y-%m-%d")

        placeholders = {
                "assistant_name" : "Xian",
                "date" : current_date,
                "user_name" : "Yan"
        }
        conversation_system_prompt = file_processor.process_file("../prompts/conversation_prompt.md", placeholders)
        response = open_ai_service.get_message_from_ai(user_message, conversation_system_prompt)
        await save_conversation(conversation_id, user_message, response, db)
        logging.info(f"{conversation_id} ==> Reply for user : {response}")
        return response
    except ValueError as e:
        logging.error(f"Error occured when generation response to user {e}")
    except Exception as e:
        logging.error(f"Error occured when generation response to user {e}")


async def save_conversation(conversation_id: str, user_message: str, response: str, db: AsyncSession ) -> None: 
    try: 
        if not conversation_id or not user_message or not response:
            raise ValueError("Conversation ID, user message, and response must not be empty.")
        conversation = ConversationSchema(
                    uuid=conversation_id,
                    user_message=user_message,
                    chat_response=response,
        )
        await conversation_crud.save_conversation(conversation, db)
    except Exception as e: 
        logging.error(f"Cannot sava conversation: {e}")
