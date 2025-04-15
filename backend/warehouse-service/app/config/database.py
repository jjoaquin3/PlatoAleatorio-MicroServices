import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from typing import AsyncGenerator

load_dotenv()

# Variables de entorno para configuración de la base de datos
POSTGRES_USER = os.getenv("POSTGRES_USER_WAREHOUSE")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD_WAREHOUSE")
POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA_WAREHOUSE")

DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

class Database:
    # Atributos de clase para motor y sesión
    engine = None
    SessionLocal = None

    @classmethod
    def get_engine(cls):
        if cls.engine is None:
            cls.engine = create_async_engine(DATABASE_URL, echo=True)
        return cls.engine

    @classmethod
    async def get_session(cls) -> AsyncGenerator:
        if cls.SessionLocal is None:
            cls.SessionLocal = sessionmaker(
                bind=cls.get_engine(),
                class_=AsyncSession,
                autocommit=False,
                autoflush=False
            )
        session = cls.SessionLocal()
        try:
            yield session
        finally:
            await session.close()