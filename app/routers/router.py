from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import get_db_session
from ..schemas.db_schemas import MemoryCreate, MemoryResponse
from ..crud.db_crud import create_memory

router = APIRouter()

@router.post("/memories/", response_model=MemoryResponse)
async def create_memory_route(memory: MemoryCreate, db: AsyncSession = Depends(get_db_session)):
    return await create_memory(db=db, memory=memory)

