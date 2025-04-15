from fastapi import APIRouter, HTTPException, Depends
from app.service.ingredient_service import IngredientService
from app.model.schema.ingredient import IngredientSchema, OrderSchemaJSON
from app.security.auth import get_api_key
from typing import List

router = APIRouter()

@router.get("/ingredients", response_model=List[IngredientSchema])
async def get_all_ingredients(
    api_key: str = Depends(get_api_key),
    ingredient_service: IngredientService = Depends()
):
    return await ingredient_service.get_all_ingredients()

@router.get("/ingredients/{name}", response_model=IngredientSchema)
async def get_ingredient_by_name(
    name: str, 
    api_key: str = Depends(get_api_key),
    ingredient_service: IngredientService = Depends()
):
    ingredient = await ingredient_service.get_ingredient_by_name(name)
    if not ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return ingredient

@router.patch("/ingredients", response_model=IngredientSchema)
async def update_stock_ingredient(    
    update_data: IngredientSchema, 
    api_key: str = Depends(get_api_key),
    ingredient_service: IngredientService = Depends()
):
    updated_ingredient = await ingredient_service.update_stock_ingredient(update_data.name, update_data.quantity)
    if not updated_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found or update failed")
    return updated_ingredient

@router.post("/ingredients/get_ingredients_by_order", response_model=OrderSchemaJSON)
async def get_ingredients_by_order(
    request: OrderSchemaJSON, 
    api_key: str = Depends(get_api_key),
    ingredient_service: IngredientService = Depends()
):    
    return await ingredient_service.get_ingredients_by_order(request)
