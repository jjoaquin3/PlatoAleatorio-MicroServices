from fastapi import APIRouter, Depends
from app.service.reports_service import ReportsService
from app.model.schema.order import OrderSchema, IngredientSchemaSimple, RecipeSchema, PurchaseSchema
from app.security.auth import get_api_key
from typing import List

router = APIRouter()

@router.get("/orders", response_model=List[OrderSchema])
async def get_orders(
    api_key: str = Depends(get_api_key),
    reports_service: ReportsService = Depends()
):
    return await reports_service.get_orders()

@router.get("/ingredients", response_model=List[IngredientSchemaSimple])
async def get_ingredients(
    api_key: str = Depends(get_api_key),
    reports_service: ReportsService = Depends()
):
    return await reports_service.get_ingredients()

@router.get("/recipes", response_model=List[RecipeSchema])
async def get_recipes(
    api_key: str = Depends(get_api_key),
    reports_service: ReportsService = Depends()
):
    return await reports_service.get_recipes()

@router.get("/purchases", response_model=List[PurchaseSchema])
async def get_market_purchases(
    api_key: str = Depends(get_api_key),
    reports_service: ReportsService = Depends()
):
    return await reports_service.get_market_purchases()

@router.post("/orders/next-id", response_model=dict)
async def get_next_order_id(
    api_key: str = Depends(get_api_key),
    reports_service: ReportsService = Depends()
):
    return await reports_service.get_next_order_id()
