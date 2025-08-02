from datetime import datetime
import logging

from sqlalchemy import exc

from ..utils import file_processor
from ..crud import conversation_crud
from app.services import token_service, open_ai_service, vector_store_service
from ..crud import db_crud
from ..repositories.interfaces import IConversationRepository

class ConversationService:
    def __init__(self, conversation_repository: IConversationRepository):
        self.conversation_repository = conversation_repository


    async def reply_user(self,user_message:str, tags:list, conversation_id:str) -> str:

        logging.info(f"Reply to user: {conversation_id} ==> User posted message: {user_message}")
        try:
            conversation = await self.conversation_repository.fetch_conversations_by_uuid(conversation_id)
        except Exception as e:
            logging.error(f"Can't reply user, cause: {e}")
        # try:       
        #     prompt = await self._build_prompt(user_message, tags, conversation_id)
        #     response = open_ai_service.get_message_from_ai(prompt)
        #     await self._save_conversation(conversation_id, user_message, response)
        #     logging.info(f"{conversation_id} ==> Ok, response generated")
        #     logging.debug(f"{conversation_id} ==> Reply for user : {response}")
        #     return response
        # except ValueError as e:
        #     logging.error(f"Error occured when generation response to user {e}")
        # except Exception as e:
        #     logging.error(f"Error occured when generation response to user {e}")


    async def _build_prompt(self,user_message: str, tags:list, conversation_id:str):

        """Build prompt consisting of system prompt,  current query from user and if applicaple conversation history 

        Args:
            user_message (str): current message from user 
            conversation_id (str): _description_
        """
        placeholders = {
            "assistant_name" : "X",
            "date" : (datetime.now()).strftime("%Y-%m-%d"),
            "user_name" : "Y"
        }
        
        conversations_list = await self._get_conversation_history(conversation_id)

        system_prompt = file_processor.process_file("../prompts/conversation_prompt.md", placeholders)
        # section for ltm 
        ## change user message to tokens 
        
        ## send query with tags to vectore store service for retreival
        long_term_memory_entry = []
        if (len(tags) > 0):
            long_term_memory= await self._search_long_term_memory(user_message, tags)
            long_term_memory_entry = [{"role": "assistant", "content": long_term_memory}]

        conversation_with_system_prompt = [{"role": "system", "content": system_prompt}] + long_term_memory_entry +  conversations_list 

        conversation_with_system_prompt.append({"role": "user", "content": user_message})

    
        logging.debug(f"Full prompt {conversation_with_system_prompt}")
        logging.info(f"Prompt without system message:  {conversation_with_system_prompt[2:]}")

        return conversation_with_system_prompt


    async def _get_conversation_history(self,conversation_id: str) -> list:
        """Retrieve conversation history for a given conversation ID.
        
        Args:
            conversation_id: The unique identifier for the conversation
            
        Returns:
            List of conversation dictionaries with 'role' and 'content' keys,
            or empty list if no conversations found
        """
        
        if not conversation_id or not isinstance(conversation_id, str):
            raise ValueError("conversation_id must be a non-empty string")
        if not conversation_id.strip():
            raise ValueError("conversation_id cannot be empty or whitespace")
        
        try: 
            conversation_history = await self.conversation_repository.fetch_conversations_by_uuid(conversation_id)
            if conversation_history: 
                logging.info(f"Adding: {len(conversation_history)} conversations to prompt")
                return conversation_history
            else:
                logging.info(f"Conversation {conversation_id}: No conversation history found")
                return []
        except Exception as e: 
            logging.error(f"Failed to fetch conversation history for {conversation_id}: {e}")
            raise

    async def _search_long_term_memory(self,user_message:str, tags: list):
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
        
        memories = await db_crud.get_memories_by_uuids(docuemnts_uuids)
        logging.info(f"Following documents will be used to generate response : {[obj.source for obj in memories]}")
        knowledge_base = ""
        for memory in memories:
            knowledge_base+=(memory.content)
        # logging.info(f"Knowledge based used for answering: {knowledge_base}")
        return knowledge_base

