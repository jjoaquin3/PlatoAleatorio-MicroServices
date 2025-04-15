from fastapi import APIRouter, Depends, HTTPException
from app.config.redis_client import RedisClient
from app.security.auth import get_api_key
from app.service.flow_service import FlowService

router = APIRouter()
flow_service = FlowService()

@router.post("/orders/next-id", response_model=dict)
def get_next_order_id(api_key: str = Depends(get_api_key)):    
    redis = RedisClient.get_client()
    next_id = redis.incr("order_id_counter")
    return {"order": next_id}

@router.post("/orders/request", response_model=dict)
async def request_order(
    order_data: dict,
    api_key: str = Depends(get_api_key)
):
    try:        
        redis = RedisClient.get_client()
        next_id = redis.incr("order_id_counter")
        #return {"order": next_id}
        order_data["order"] = next_id
    
        result = await flow_service.handle_order_request(order_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
