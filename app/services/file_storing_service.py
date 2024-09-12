from ..schemas.db_schemas import MemoryCreate
from fastapi import  Depends, UploadFile
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db_session
from app.crud.db_crud import save_memory
import re
from .token_service import convert_into_embeddings, EmbeddingError
from .vector_store_service import save_document_to_vector_store
from .taging_service import tag_document, TagingError


async def store_memory(message: str, file: UploadFile, client_uuid: str = None, db: AsyncSession = Depends(get_db_session)):    
    # FIXME #25 remove client uuid usage nad creation from this class 
  
    try:
   
        memory_document = await create_memory(message, file, client_uuid)
        embedded_document = convert_into_embeddings(memory_document.content)

        if not is_valid_for_processing(memory_document, embedded_document):
            logging.warning("Invalid input parameters, skipping processing.")
            return

        await save_memory(db=db, memory=memory_document)
        save_document_to_vector_store(embedded_document, memory_document.source, str(memory_document.uuid), memory_document.tags) 
        logging.info(f"Message processed sucesfully uuid: {memory_document.uuid}, stored text: {memory_document.name}")
    
    except Exception as e: 
        logging.error(f"Cannot store memory {str(e)}")


async def create_memory(message: str, file: UploadFile, client_uuid: str = None,) -> MemoryCreate:
    """ Based on provided file create MemoryCreate object

    Args:
        message (str): user message 
        file (UploadFile): file to be saved
        client_uuid (str, optional): uuid . Defaults to None.

    Returns:
        _type_: MemoryCreate
    """
    try: 
        file_content, file_name = await get_file_data(file )
        new_memory = MemoryCreate(
                name=message,
                content=file_content,
                active=True,
                source=file_name
        )
        # FIXME #25 remove client uuid usage nad creation from this class 
        process_uuid(new_memory, client_uuid)

        tags = tag_document(new_memory.content, False)
        new_memory.tags = tags
        return new_memory

    except FileReadError as fre:
        logging.error(f"Cannot store memory Error code: {fre.error_code} message: {fre.message}")
    except EmbeddingError as er:
        logging.error(f"Cannot store memory Error code: {er.error_code} message: {er.message}")
    except TagingError as te: 
        logging.error(f"Cannot store memory Error code: {te.error_code} message: {te.message}")


def process_uuid(memory: MemoryCreate, client_uuid : str) -> None: 
     
    # FIXME #25 remove client uuid usage nad creation from this class 
    

     if client_uuid != None and is_uuid_valid(client_uuid):
            memory.uuid = client_uuid

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
        raise FileReadError("Error while reading file: {e}", 1000)


def is_uuid_valid(uuid: str ) -> bool:
    # FIXME #25 remove client uuid usage nad creation from this class 

    regex = re.compile('^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}\Z', re.I)
    match = regex.match(uuid)
    return bool(match)

def is_valid_for_processing(new_memory, embedded_document):
    return bool(len(new_memory.tags) > 0  and embedded_document and new_memory and new_memory.uuid)


#### CUSTOM ERRORS 


class FileReadError(Exception):
    """Exception raised for errors in the file read process.
       error code = 1000
    """

    def __init__(self, message, error_code):
        super().__init__(message)
        self.error_code = error_code
