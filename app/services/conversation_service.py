from datetime import datetime
import logging

from ..utils import file_processor
from ..services import open_ai_service

def reply_user(user_message:str, conversation_id:str) -> str:
    
    logging.info(f"{conversation_id} ==> User posted message: {user_message}")
    current_date = (datetime.now()).strftime("%Y-%m-%d")

    placeholders = {
            "assistant_name" : "Xian",
            "date" : current_date,
            "user_name" : "Yan"
    }
    conversation_system_prompt = file_processor.process_file("../prompts/conversation_prompt.md", placeholders)
    response = open_ai_service.get_message_from_ai(user_message, conversation_system_prompt)

    logging.info(f"{conversation_id} ==> Reply for user : {response}")

    # save request - response - conversation id to database 
