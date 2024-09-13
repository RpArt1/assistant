import logging
from qdrant_client.http.models import PointStruct
from datetime import datetime
from qdrant_client.http.models import Filter, FieldCondition, MatchAny, SearchRequest

from app.utils.env_settings import  QDRANT_COLLECTION
from app.dependencies import vector_store_client


def fetch_documents_uuids_from_vector_store(embedded_query: list, tags: list, top_k: int = 2):
    try:
        tag_filter = Filter(
            must=[
                FieldCondition(
                    key="tags.pre_defined_tags",
                    match=MatchAny(any=tags) 
                )
            ]
        )
        
             
        search_results = vector_store_client.search(
            collection_name=QDRANT_COLLECTION,
            query_vector=embedded_query,
            query_filter=tag_filter,
            limit=top_k,
            score_threshold=0.3
        )
        
        
        uuids = [result.id for result in search_results]
                
        if not uuids:
            logging.info("QDRANT: No matching entries found for the query and tags.")
            return None
        
        logging.info(f"Found matching documents with UUIDs: {uuids}")
        return uuids
    
    except Exception as e:
        logging.error(f"Error during fetching from vector store: {e}")
        return None


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

