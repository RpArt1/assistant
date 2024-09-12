from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any
import json
import logging


from ..models.db_models import Memory
from ..schemas.db_schemas import MemoryCreate, MemoryResponse

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


async def get_memories_by_uuids(uuid_list: list[str], db: AsyncSession) -> list[MemoryResponse]:
    try:
        query = select(Memory).where(Memory.uuid.in_(uuid_list))
        result = await db.execute(query)
        memories = result.scalars().all()

        memory_responses = [
            MemoryResponse(
                id=memory.id,
                uuid=memory.uuid,
                name=memory.name,
                content=memory.content,
                reflection=memory.reflection,
                tags=(json.loads(memory.tags) if isinstance(memory.tags, str) else memory.tags).get("pre_defined_tags", []),
                source=memory.source,
                created_at=memory.created_at,
                active=memory.active if memory.active is not None else False,
            )
            for memory in memories
        ]
        
        return memory_responses

    except Exception as e:
        logging.error(e)
        return []