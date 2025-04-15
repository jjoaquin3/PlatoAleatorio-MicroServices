from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import Database

async def get_db_client(session: AsyncSession = Depends(Database.get_session)):
    try:
        yield session
    finally:
        pass 