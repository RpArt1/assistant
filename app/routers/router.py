import uuid
from fastapi import APIRouter, UploadFile
import logging


router = APIRouter()


@router.post("/")
async def create_memory(message: str, client_uuid: str = None,  file: UploadFile = None):

    try:
        if client_uuid is None:
            message_uuid = str(uuid.uuid4())
        else: 
            message_uuid = client_uuid
            
        logging.info(f"Message processed sucesfully uuid: {message_uuid}, stored text: {message}")
        return {"message": "Data stored successfully", "uuid": message_uuid, "stored text": message}
    
    except Exception as e: 
        logging.ERROR(e, ext_info=True)

