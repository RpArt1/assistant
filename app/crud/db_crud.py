from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..models.db_models import Memory
from ..schemas.db_schemas import MemoryCreate
from typing import Any
import json
import logging

async def save_memory(db: AsyncSession, memory: MemoryCreate) -> Memory:
    try:
        db_memory = Memory(
            uuid=memory.uuid,
            name=memory.name,
            content=memory.content,
            reflection=memory.reflection,
            tags=json.dumps(memory.tags),
            active=memory.active,
            source=memory.source
        )
        db.add(db_memory)
        await db.commit()
        await db.refresh(db_memory)
        
        db_memory.tags = json.loads(db_memory.tags)
        return db_memory
     
    except Exception as e: 
        logging.error(e)
