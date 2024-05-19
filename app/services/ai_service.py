from typing import List
from pydantic import BaseModel, Field
from typing import Literal
import json
import enum
from openai import OpenAI
from os import environ
import logging
from ..utils import file_processor

class ToolEnum (str,enum.Enum):
    MEMO = "memory"
    TODO = "todo"

class TagEnum (str,enum.Enum):
    BRAIN = "brain"
    PSYCHOLOGY = "psychology"
    AI = "ai"
    PYTHON = "python"
    TODO = "todo"
    MEMORY = "memory"
    TONY = "tony"
    OTHER = "other"

#TYPES 
class TypeEnum(str, enum.Enum):
    QUERY = "query"
    ACTION = "action"

class QueryModel(BaseModel):
    type : TypeEnum = Field(default=TypeEnum.QUERY, description="classification type")
    tags :  TagEnum = Field(...)

class ActionModel(BaseModel):
    type : TypeEnum = Field(default=TypeEnum.ACTION, description="classification type")
    tool : ToolEnum = Field(...)
    content : str


# Create two possible functions to choose from: 
function_list = [
    {
        "name" : "query",
        "description" : "Categorises user message as query, if none tag is matching choose other",
        "parameters" : QueryModel.model_json_schema(),
        "required": ["type", "tags"]
    },
    {
        "name": "action",
        "description": "Categorises user message as action to be done and fills proper fields specified in required",
        "parameters": ActionModel.model_json_schema(),
        "required": ["type", "tool", "content"]
    }
]


def categorise_user_query(message: str ):
    """ First place where user query is processed and catagorized 

    Args:
        message (str): user message
    """
    try:
        categorisation_system_prompt = file_processor.process_file("../prompts/categorisation_prompt.md")
        user_query_categorisation = call_ai(message, categorisation_system_prompt, function_list)

        message_type = user_query_categorisation.get('type')
        tags = user_query_categorisation.get('tags')
        tool = user_query_categorisation.get('tool')
        content = user_query_categorisation.get('content')
        logging.info(f"Query categorised : message type: {message_type}, tags: {tags}, tool: {tool}, content {content}")


    except (FileNotFoundError, KeyError, Exception) as e:
        logging.error(f"User query cannot be categorised")


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



