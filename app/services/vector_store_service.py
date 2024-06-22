import logging
from qdrant_client.http.models import PointStruct
from datetime import datetime

from app.utils.env_settings import  QDRANT_COLLECTION
from app.dependencies import vector_store_client





def save_document_to_vector_store(embedded_document: list, file_name: str, uuid_str : str, tags: list) :
    try:

        point = PointStruct(
            id=uuid_str, 
            vector=embedded_document, 
            payload={"file_name": file_name, 
                     "tags" : tags,
                     "creation_time" : datetime.now()
                     } 
        )
    
        operation_info = vector_store_client.upsert(
            collection_name=QDRANT_COLLECTION,
            wait=True,
            points=[point],
        )
        logging.info(f"Result = {operation_info}")
    
    except Exception as e:
        logging.error(f"Coudn't save to vector store: {e}")

