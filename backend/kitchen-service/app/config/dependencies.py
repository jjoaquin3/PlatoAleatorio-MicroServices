from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient
from app.config.database_nosql import MongoDBConfig

async def get_mongo_client():
    db_config = MongoDBConfig()
    client = await db_config.get_client()  # Llamada asíncrona para obtener el cliente de Motor
    try:
        yield client
    finally:
        await db_config.close_connection()  # Cerrar la conexión asíncrona
