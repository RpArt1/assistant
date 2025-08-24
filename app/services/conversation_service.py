from datetime import datetime
import logging

from sqlalchemy import exc

from app.repositories import conversation_repository
from app.services.interfaces.interfaces import  ILlmService

from ..utils import file_processor
from ..crud import db_crud
from ..repositories.interfaces import IConversationRepository
from ..domain.conversation import MessageRole, Conversation

class ConversationService:
    def __init__(self, conversation_repository: IConversationRepository, llm_service: ILlmService):
        self.conversation_repository = conversation_repository
        self.llm_service = llm_service

    async def reply_user(self,user_message:str, tags:list, conversation_id:str) -> str:
        try:
            conversation = await self.conversation_repository.get_conversation(conversation_id)
            # create new conversation if not exists and add message  
            if not conversation:
                conversation = Conversation()
                conversation.add_message(MessageRole.SYSTEM, self._build_system_prompt())
            
            conversation.add_message(MessageRole.USER, user_message)
            # search for relevant documents
            # get response from ai
            conversations_formated = conversation.prepare_messages()
            response = self.llm_service.get_message_from_ai(conversations_formated)
            if response:
                logging.info(f"{conversation_id} ==> Ok, response generated")
                logging.debug(f"{conversation_id} ==> Reply for user : {response}")
                conversation.add_message(MessageRole.ASSISTANT, response)
            await self.conversation_repository.save_conversation(conversation)
            return response
        except ValueError as e:
            logging.error(f"Error occured when generation response to user {e}")
        except Exception as e:
            logging.error(f"Error occured when generation response to user {e}")

    def _build_system_prompt(self):
        placeholders = {
            "assistant_name" : "X",
            "date" : (datetime.now()).strftime("%Y-%m-%d"),
            "user_name" : "Y"
        }
        system_prompt = file_processor.process_file("../prompts/conversation_prompt.md", placeholders)
        return system_prompt

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

