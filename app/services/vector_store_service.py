import logging
from qdrant_client.http.models import PointStruct
from datetime import datetime

from app.utils.env_settings import  QDRANT_COLLECTION
from app.dependencies import vector_store_client





def save_document_to_vector_store(embedded_document: list, file_name: str, uuid_str : str, tags: list) :
    try:
        current_time = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")

        point = PointStruct(
            id=uuid_str, 
            vector=embedded_document, 
            payload={"file_name": file_name, 
                     "tags" : tags,
                     "creation_time" : current_time
                     } 
        )
    
        operation_info = vector_store_client.upsert(
            collection_name=QDRANT_COLLECTION,
            wait=True,
            points=[point],
        )
        logging.info(f"Document with uuid={uuid_str} was processed to QDRANT with satus = {str(operation_info.status)}")
    
    except Exception as e:
        logging.error(f"Coudn't save to vector store: {e}")

