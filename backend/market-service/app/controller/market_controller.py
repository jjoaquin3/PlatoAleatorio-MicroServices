from fastapi import APIRouter, Depends, HTTPException
from app.security.auth import get_api_key
from app.model.schema.purchase import PurchaseRequest, PurchaseSchema
from app.service.market_service import MarketService
from typing import List

router = APIRouter()

@router.get("/market/purchases", response_model=List[PurchaseSchema])
async def get_all_purchases(
    api_key: str = Depends(get_api_key),
    market_service: MarketService = Depends()
):
    return await market_service.get_all_purchases()

@router.post("/market/purchases", response_model=dict)
async def purchase_ingredient(
    request: PurchaseRequest, 
    api_key: str = Depends(get_api_key),
    market_service: MarketService = Depends()
):
    result = await market_service.process_purchase(request)    
    if result['status'] == 'failure':
        raise HTTPException(status_code=400, detail="Ingredient not available")    
    return result