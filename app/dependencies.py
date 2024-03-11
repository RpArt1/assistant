from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
import logging
load_dotenv()

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")
engine = create_async_engine(DB_CONNECTION_STRING, echo=True) # echo set to TRUE logs sql TODO: move it to configureation 

AsyncSessionLocal = sessionmaker( # factory for asynchronous session objects.
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)

async def get_db_session(): 
    async with AsyncSessionLocal() as session:
        yield session #ensures that each request gets its own session, isolated from other requests
