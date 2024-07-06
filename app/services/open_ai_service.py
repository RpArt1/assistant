import logging
import json

from openai import OpenAI
from os import environ


def call_ai(message: str, system_prompt: str, function_list: list=None): 
    """Function responsible for direct comunication to openai 

    Args:
        message (str): user message
        system_prompt (str): system prompt that will be used 
        function_list (list, optional): list of available functions. Defaults to None.
    """

    try:
        client = OpenAI(api_key=environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
            ],
            functions=function_list,
            function_call="auto"
        )
        # fetch data from output 
        response = response.choices[0].message

        if (response.function_call is not None and response.function_call.arguments is not None ):
            function_arguments = json.loads(response.function_call.arguments) 
            logging.info(f"Output from ai => {function_arguments}")
            return function_arguments
        else: 
            logging.debug(f"Message returned : {response} ")
            raise OpenAiError(f"No fuction was called during openai call")

    except Exception as e: 
        raise OpenAiError(f"Call to ai ended up with failure, details: {e},")


def get_message_from_ai(message: str, system_prompt: str): 
    """Function responsible for direct comunication to openai 

    Args:
        message (str): user message
        system_prompt (str): system prompt that will be used 
    """

    try:
        client = OpenAI(api_key=environ.get('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
            ],
        )
        response = response.choices[0].message.content
        return response
     
    except Exception as e: 
        raise OpenAiError(f"Call to ai ended up with failure, details: {e},")

class OpenAiError(Exception):
    """Exception raised for errors conected to open ai api
       error code = 1003
    """

    def __init__(self, message):
        super().__init__(message)
        self.error_code = 1003
