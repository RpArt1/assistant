from enum import Enum

class ToolEnum (str, Enum):
    MEMORY = "memory"
    TODO = "todo"

class TagEnum (str, Enum):
    BRAIN = "brain"
    PSYCHOLOGY = "psychology"
    AI = "ai"
    PYTHON = "python"
    TODO = "todo"
    MEMORY = "memory"
    XIO = "Xio"

#TYPES 
class TypeEnum(str,  Enum):
    QUERY = "query"
    ACTION = "action"

