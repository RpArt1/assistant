from typing import List
from pydantic import BaseModel, Field
from typing import Literal
import json
from enum import Enum
from openai import OpenAI
from os import environ
import logging
from ..utils import file_processor
from ..utils.enums import TypeEnum, ToolEnum, TagEnum


class QueryModel(BaseModel):
    type : TypeEnum = Field(default=TypeEnum.QUERY, description="classification type")
    tags: List[TagEnum] = Field(..., description="Tags related to the message")

class ActionModel(BaseModel):
    type : TypeEnum = Field(default=TypeEnum.ACTION, description="classification type")
    tools: List[ToolEnum] = Field(..., description="Tools related to the message")
    content: str = Field(..., description="Content of the action")


# Create two possible functions to choose from: 
function_list = [
    {
        "name" : "classify_as_query",
        "description" : "Categorises user message as query",
        "parameters" : QueryModel.model_json_schema(),
        "required": ["type", "tags"]
    },
    {
        "name": "clasify_as_action",
        "description": "Categorizes user message as an action to be done and fills in the required fields.",
        "parameters": ActionModel.model_json_schema(),
        "required": ["type", "tool", "content"]
    }
]


def categorise_user_query(message: str, mock: bool ):
    """ First place where user query is processed and catagorized 

    Args:
        message (str): user message
        mock (bool) : flag used for development purposes if call to external system is not required
    """
    if mock: 

        mock_expected_action_categorisation = {'type': 'action', 'tools': ['memory'], 'content': ['store attachment']}
        mock_expected_query_categorisation = {'type': 'query', 'tags': ['ai']}

        return mock_expected_action_categorisation

    try:
        logging.info(f"Query: {message}")
        categorisation_system_prompt = file_processor.process_file("../prompts/categorisation_prompt.md")
        user_query_categorisation = call_ai(message, categorisation_system_prompt, function_list)
        logging.info(f"Query categorization : {user_query_categorisation}")
        return user_query_categorisation
    except (FileNotFoundError, KeyError, Exception) as e:
        logging.error(f"Query cannot be categorised")


def call_ai(message: str, system_prompt: str, function_list: list=None): 
    """Function responsible for direct comunication to openai 

    Args:
        message (str): user message
        system_prompt (str): system prompt that will be used 
        function_list (list, optional): list of available functions. Defaults to None.
    """

    ## TODO call_ai should be moved to another class - its generic method 
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
            logging.error("No function was choosen, response content: {response.content} ")
            raise Exception
    except Exception as e: 
        logging.error(f"Call to ai ended up with failure, details: {e}")
        raise



