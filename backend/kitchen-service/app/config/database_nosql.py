import os
from motor.motor_asyncio import AsyncIOMotorClient  # Importar Motor para operaciones asincrónicas
from pymongo.errors import ServerSelectionTimeoutError

class MongoDBConfig:
    
    def __init__(self):
        self.mongo_user = os.getenv("MONGO_INITDB_ROOT_USERNAME")
        self.mongo_password = os.getenv("MONGO_INITDB_ROOT_PASSWORD")
        self.mongo_db = os.getenv("MONGO_DB")
        self.mongo_host = os.getenv("MONGO_HOST")
        self.mongo_port = os.getenv("MONGO_PORT")
        self.client = None

    async def get_client(self):
        if not self.client:
            try:
                mongo_uri = f"mongodb://{self.mongo_user}:{self.mongo_password}@{self.mongo_host}:{self.mongo_port}/"
                # Usamos Motor para las conexiones asíncronas
                self.client = AsyncIOMotorClient(mongo_uri)
                # Verifica la conexión
                await self.client.admin.command('ping')
            except ServerSelectionTimeoutError as e:
                raise Exception(f"Error al conectar a MongoDB: {e}")
        return self.client[self.mongo_db]

    async def close_connection(self):
        if self.client:
            self.client.close()
            self.client = None
