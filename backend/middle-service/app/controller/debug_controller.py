from fastapi import APIRouter, Depends
from app.config.redis_client import RedisClient
from app.security.auth import get_api_key

import json

router = APIRouter()

@router.get("/debug/queues", response_model=dict)
def get_redis_queues(api_key: str = Depends(get_api_key)):
    redis = RedisClient.get_client()

    market_queue = redis.lrange("market_queue", 0, -1)
    retry_queue = redis.lrange("market_retry_queue", 0, -1)

    def parse_items(queue):
        return [json.loads(i) for i in queue]

    return {
        "market_queue": parse_items(market_queue),
        "market_retry_queue": parse_items(retry_queue)
    }
