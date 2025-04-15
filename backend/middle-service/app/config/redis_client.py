import os
import redis
from dotenv import load_dotenv

load_dotenv()

class RedisClient:
    _client = None

    @classmethod
    def get_client(cls):
        if cls._client is None:
            cls._client = redis.Redis(
                host=os.getenv("REDIS_HOST", "localhost"),
                port=int(os.getenv("REDIS_PORT", 6379)),
                db=0,
                decode_responses=True  # Retorna strings en lugar de bytes
            )
        return cls._client

    @classmethod
    def close(cls):
        if cls._client:
            cls._client.close()
            cls._client = None
