import logging
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, UploadFile, Depends
from io import BytesIO

from ..utils import file_processor
from ..services.ai_service import categorise_user_query
from ..services.file_storing_service import store_memory
from ..utils.enums import ToolEnum
from ..dependencies import get_db_session


router = APIRouter()


@router.post("/")
async def process_user_query(message: str, client_uuid: str = None,  file: UploadFile = None, db: AsyncSession = Depends(get_db_session)):
    """ Main endpoint to which all user queries are sent, acts as router which determines which action should be taken

    Args:
        message (str): user message 
        client_uuid (str, optional): conversetion id . Defaults to None.
        file (UploadFile, optional): file to be uploaded to memory . Defaults to None.
        db (AsyncSession, optional): databse session. Defaults to Depends(get_db_session).
    """
    use_mock = False
    user_query_categorisation = categorise_user_query(message, use_mock)
    if use_mock is True: 
        file = mock_file()
        

    # if user_query_categorisation contains filed tool and its value is "MEMORY" then save to database 

    if 'tools' in user_query_categorisation and ToolEnum.MEMORY.value in user_query_categorisation['tools']:
        await store_memory(message, file, client_uuid, db)



def mock_file(): 
    ## short file
    file_name = "mock.txt"
    file_content = "Sample file content"
    ## for tagging
    file_name = "taging-test-document.txt"
    file_content =  file_processor.process_file(file_name, None, "misc")


    byte_file_content = file_content.encode('utf-8')

    file_bytes_io = BytesIO(byte_file_content)
    return UploadFile(filename=file_name, file=file_bytes_io)
