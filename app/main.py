from fastapi import FastAPI, Request, status
import logging
from .routers import router
from .routers import test_router
import debugpy
from fastapi.exceptions import RequestValidationError
from qdrant_client import QdrantClient
from qdrant_client.http.models import  VectorParams, Distance
from .utils.env_settings import QDRANT_API_KEY, QDRANT_URL, QDRANT_COLLECTION


# logging configuration

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
)
logger = logging.getLogger(__name__)

# Debuger 

debugpy.listen(("0.0.0.0", 5678))
debugpy.wait_for_client()

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

client = QdrantClient(
    QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=True,
)


@app.on_event("startup")
async def startup_event():
    
    # Check if the collection exists
    collections = client.get_collections()
    if QDRANT_COLLECTION not in [collection.name for collection in collections.collections]:
        # Create collection if it does not exist
        client.create_collection(
            collection_name=QDRANT_COLLECTION,
            vectors_config=VectorParams(size=4, distance=Distance.DOT)
        )
        logger.info(f"Collection '{QDRANT_COLLECTION}' created.")
    else:
        logger.info(f"Collection '{QDRANT_COLLECTION}' created.")

        