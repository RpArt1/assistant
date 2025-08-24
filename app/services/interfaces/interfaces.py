from typing import Protocol

class ILlmService(Protocol):
    def get_message_from_ai(conversation_with_system_prompt: list): 
        ...