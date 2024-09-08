from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends

from ..utils import file_processor
from ..crud import conversation_crud
from ..dependencies import get_db_session
from ..schemas.conversation_schema import ConversationSchema
from app.services import conversation_history_service, token_service, open_ai_service



async def reply_user(user_message:str, conversation_id:str, db: AsyncSession = Depends(get_db_session)) -> str:
    try: 
        logging.info(f"{conversation_id} ==> User posted message: {user_message}")
        
        prompt = await build_prompt(user_message, conversation_id, db)
      
        response = open_ai_service.get_message_from_ai(prompt)

        await save_conversation(conversation_id, user_message, response, db)

        logging.info(f"{conversation_id} ==> Reply for user : {response}")

        return response
    
    except ValueError as e:
        logging.error(f"Error occured when generation response to user {e}")

    except Exception as e:
        logging.error(f"Error occured when generation response to user {e}")


async def build_prompt(user_message: str, conversation_id:str, db):

    """Build prompt consisting of system prompt,  current query from user and if applicaple conversation history 

    Args:
        user_message (str): current message from user 
        conversation_id (str): _description_
        db (_type_): _description_
    """
    placeholders = {
        "assistant_name" : "Xian",
        "date" : (datetime.now()).strftime("%Y-%m-%d"),
        "user_name" : "Yan"
    }
    
    conversations_list = get_conversation_history(conversation_id, db)

    system_prompt = file_processor.process_file("../prompts/conversation_prompt.md", placeholders)

    conversation_with_system_prompt = [{"role": "system", "content": system_prompt}] + conversations_list 

    conversations_list.append({"role": "user", "content": user_message})

    # section for ltm 
    ## change user message to tokens 
    embedded_user_query = token_service.get_embeddings(user_message)
    
    ## send query with tags to vectore store service for retreival 

    return conversation_with_system_prompt


async def get_conversation_history(conversation_id, db):
    searched_conversations_list = await conversation_history_service.fetch_conversations_by_uuid(conversation_id, db)

    if(len(searched_conversations_list) > 0 ): 

        logging.info(f"Adding: {len(searched_conversations_list)} conversations to prompt")
        conversations_list = searched_conversations_list
    else:
        logging.info(f"No converastions found")
        return []


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
