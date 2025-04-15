from app.repository.recipe_repository import RecipeRepository
from fastapi import Depends

class RecipeService:
    def __init__(self, recipe_repository: RecipeRepository = Depends()):
        self.recipe_repository = recipe_repository

    async def get_recipe_by_recipe(self, recipe: str):        
        return await self.recipe_repository.get_recipe_by_recipe(recipe)
    
    async def get_all_recipes(self):
        return await self.recipe_repository.get_all_recipes()
