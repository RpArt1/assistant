from ..dependencies import get_db_session
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..services.ai_service import categorise_user_query
from ..services.file_storing_service import store_memory
from fastapi import APIRouter, UploadFile, Depends
from ..utils.enums import ToolEnum
from io import BytesIO


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
    use_mock = True
    user_query_categorisation = categorise_user_query(message, use_mock)
    if use_mock is True: 
        file_content = b"Sample file content"
        file_like = BytesIO(file_content)
        file = UploadFile(filename="test_file.txt", file=file_like)

    # if user_query_categorisation contains filed tool and its value is "MEMORY" then save to database 

    if 'tools' in user_query_categorisation and ToolEnum.MEMORY.value in user_query_categorisation['tools']:
        await store_memory(message, file, client_uuid, db)

