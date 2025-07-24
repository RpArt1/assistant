from datetime import datetime
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import  Depends

from ..utils import file_processor
from ..crud import conversation_crud
from ..dependencies import get_db_session
from ..schemas.conversation_schema import ConversationSchema
from app.services import conversation_history_service, token_service, open_ai_service, vector_store_service
from ..crud import db_crud


async def reply_user(user_message:str, tags:list, conversation_id:str, db: AsyncSession = Depends(get_db_session)) -> str:

    logging.info(f"{conversation_id} ==> User posted message: {user_message}")

    try:       
        prompt = await build_prompt(user_message, tags, conversation_id, db)
        response = open_ai_service.get_message_from_ai(prompt)
        await save_conversation(conversation_id, user_message, response, db)
        logging.info(f"{conversation_id} ==> Reply for user : {response}")
        return response
    
    except ValueError as e:
        logging.error(f"Error occured when generation response to user {e}")
    except Exception as e:
        logging.error(f"Error occured when generation response to user {e}")


async def build_prompt(user_message: str, tags:list, conversation_id:str, db):

    """Build prompt consisting of system prompt,  current query from user and if applicaple conversation history 

    Args:
        user_message (str): current message from user 
        conversation_id (str): _description_
        db (_type_): _description_
    """
    placeholders = {
        "assistant_name" : "X",
        "date" : (datetime.now()).strftime("%Y-%m-%d"),
        "user_name" : "Y"
    }
    

    conversations_list = await get_conversation_history(conversation_id, db)

    system_prompt = file_processor.process_file("../prompts/conversation_prompt.md", placeholders)
    # section for ltm 
    ## change user message to tokens 
    
    ## send query with tags to vectore store service for retreival
    long_term_memory_entry = []
    if (len(tags) > 0):
        long_term_memory= await search_long_term_memory(user_message, tags, db)
        long_term_memory_entry = [{"role": "assistant", "content": long_term_memory}]

    conversation_with_system_prompt = [{"role": "system", "content": system_prompt}] + long_term_memory_entry +  conversations_list 

    conversation_with_system_prompt.append({"role": "user", "content": user_message})

  
    logging.debug(f"Full prompt {conversation_with_system_prompt}")
    logging.info(f"Prompt without system message:  {conversation_with_system_prompt[2:]}")

    return conversation_with_system_prompt


async def get_conversation_history(conversation_id: str, db: AsyncSession) -> list:
    """Retrieve conversation history for a given conversation ID.
    
    Args:
        conversation_id: The unique identifier for the conversation
        db: Database session for async operations
        
    Returns:
        List of conversation dictionaries with 'role' and 'content' keys,
        or empty list if no conversations found
    """
    
    if not conversation_id or not isinstance(conversation_id, str):
        raise ValueError("conversation_id must be a non-empty string")
    if not conversation_id.strip():
        raise ValueError("conversation_id cannot be empty or whitespace")
    
    try: 
        conversation_history = await conversation_history_service.fetch_conversations_by_uuid(conversation_id, db)
        if conversation_history: 
            logging.info(f"Adding: {len(conversation_history)} conversations to prompt")
            return conversation_history
        else:
            logging.info(f"Conversation {conversation_id}: No conversation history found")
            return []
    except Exception as e: 
        logging.error(f"Failed to fetch conversation history for {conversation_id}: {e}")
        raise

async def search_long_term_memory(user_message:str, tags: list, db:AsyncSession):
    """embbed user query and search similary in vector store limiting search to region specified in tags

    Args:
        user_message (str): message
        tags (list): tags

    Returns:
        _type_: ???? TODO ARTUR
    """

    embedded_user_query = token_service.get_embeddings(user_message)
    docuemnts_uuids = vector_store_service.fetch_documents_uuids_from_vector_store(embedded_user_query, tags)
    # find entries in db based on returned uuids 
    if docuemnts_uuids is None or len(docuemnts_uuids) == 0: 
        return []
    
    memories = await db_crud.get_memories_by_uuids(docuemnts_uuids, db)
    logging.info(f"Following documents will be used to generate response : {[obj.source for obj in memories]}")
    knowledge_base = ""
    for memory in memories:
        knowledge_base+=(memory.content)
    # logging.info(f"Knowledge based used for answering: {knowledge_base}")
    return knowledge_base


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
