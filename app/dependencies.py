from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from .utils.env_settings import DB_CONNECTION_STRING
from fastapi import Depends

from .services.conversation_service import ConversationService
from .repositories.interfaces import IConversationRepository
from .repositories.conversation_repository import SQLAlchemyConversationRepository

engine = create_async_engine(DB_CONNECTION_STRING, echo=False) # echo set to TRUE logs sql TODO: move it to configureation 

AsyncSessionLocal = sessionmaker( # factory for asynchronous session objects.
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db_session(): 
    async with AsyncSessionLocal() as session:
        yield session #ensures that each request gets its own session, isolated from other requests


## Depnedncy injection for history repository

def get_conversation_repository(db: AsyncSession = Depends(get_db_session)) -> IConversationRepository:
    return SQLAlchemyConversationRepository(db)

def get_conversation_service(
    repository: IConversationRepository = Depends(get_conversation_repository)
)->ConversationService:
    return ConversationService(repository)
