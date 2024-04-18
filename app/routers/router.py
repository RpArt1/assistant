import uuid
from fastapi import APIRouter, Depends, UploadFile
from app.crud.db_crud import save_memory
from ..dependencies import get_db_session
import logging
from ..schemas.db_schemas import MemoryCreate
from sqlalchemy.ext.asyncio import AsyncSession
import re

router = APIRouter()


@router.post("/")
async def create_memory(message: str, client_uuid: str = None,  file: UploadFile = None, db: AsyncSession = Depends(get_db_session)):

    try:
        file_content, file_name = await get_file_data(file )

        new_memory = MemoryCreate(
            name=message,
            content=file_content,
            active=True,
            source=file_name
        )
        if client_uuid != None and is_uuid_valid(client_uuid):
            new_memory.uuid = client_uuid
        await save_memory(db=db, memory=new_memory)
        
        logging.info(f"Message processed sucesfully uuid: {new_memory.uuid}, stored text: {new_memory.name}")

    except Exception as e: 
        logging.error(e)


async def get_file_data(file: UploadFile = None) -> str: 
    """if file is present return its content and file name

    Args:
        file (UploadFile, optional): _description_. Defaults to None.

    Returns:
        str: file content, filename
    """
    try:
        if ( file == None):
            return None, None
        contents = await file.read()
        file_str = contents.decode()
        file_name = file.filename

        return file_str, file_name
    except Exception as e: 
        logging.error(f"Error while reading file: {e}")

def is_uuid_valid(uuid: str ) -> bool: 
    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)