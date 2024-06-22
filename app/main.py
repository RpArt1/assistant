from fastapi import FastAPI, Request
import logging
import debugpy
from fastapi.exceptions import RequestValidationError
from qdrant_client.http.models import  VectorParams, Distance


from app.routers import router, test_router
from app.utils.env_settings import  QDRANT_COLLECTION
from app.dependencies import vector_store_client

# logging configuration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)

# Debuger 

debugpy.listen(("0.0.0.0", 5678))
# debugpy.wait_for_client() # ENABLE if you want app startup being dependant on debug startup

# application 

app = FastAPI()

    # exception handling 

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return exc

    # Available routers for app 

app.include_router(router.router, prefix="/memories", tags=["memories"])
app.include_router(test_router.router, prefix="/test", tags=["testing"])


# Qdrant



@app.on_event("startup")
async def startup_event():
    
    # Check if the collection exists
    collections = vector_store_client.get_collections()
    if QDRANT_COLLECTION not in [collection.name for collection in collections.collections]:
        # Create collection if it does not exist
        vector_store_client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=1536, distance=Distance.DOT)
        )
        logger.info(f"Collection '{QDRANT_COLLECTION}' created.")
    else:
        logger.info(f"Collection '{QDRANT_COLLECTION}' created.")

        