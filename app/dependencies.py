from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .utils.env_settings import DB_CONNECTION_STRING


from qdrant_client import QdrantClient
from .utils.env_settings import QDRANT_API_KEY, QDRANT_URL


engine = create_async_engine(DB_CONNECTION_STRING, echo=False) # echo set to TRUE logs sql TODO: move it to configureation 

AsyncSessionLocal = sessionmaker( # factory for asynchronous session objects.
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db_session(): 
    async with AsyncSessionLocal() as session:
        yield session #ensures that each request gets its own session, isolated from other requests



#### QDRANT 

vector_store_client = QdrantClient(
    QDRANT_URL,
    api_key=QDRANT_API_KEY,
    prefer_grpc=True,
)

