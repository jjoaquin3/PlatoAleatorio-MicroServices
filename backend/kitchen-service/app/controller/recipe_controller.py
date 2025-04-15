from fastapi import APIRouter, HTTPException, Depends
from app.service.recipe_service import RecipeService
from app.model.schema.recipe import RecipeSchema
from app.security.auth import get_api_key
from typing import List

router = APIRouter()

@router.get("/recipes/{recipe}/", response_model=dict)
@router.get("/recipes/{recipe}", response_model=dict)
async def get_recipe_by_recipe(
    recipe: str, 
    api_key: str = Depends(get_api_key),  
    recipe_service: RecipeService = Depends()  # Inyección del Servicio
):    
    recipe_data = await recipe_service.get_recipe_by_recipe(recipe)    
    if recipe_data:
        return recipe_data
    raise HTTPException(status_code=404, detail="Recipe not found")

@router.get("/recipes", response_model=List[RecipeSchema])
@router.get("/recipes/", response_model=List[RecipeSchema])
async def get_all_recipes(
    api_key: str = Depends(get_api_key),
    ingredient_service: RecipeService = Depends()
):
    return await ingredient_service.get_all_recipes()
