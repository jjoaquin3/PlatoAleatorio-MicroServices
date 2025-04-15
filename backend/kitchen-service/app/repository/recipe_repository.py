from app.config.dependencies import get_mongo_client
from motor.motor_asyncio import AsyncIOMotorCollection  # Usamos Motor en lugar de pymongo
from app.model.recipe import Recipe
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

class RecipeRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
        self.db = mongo_client                  # Se inyecta la conexión a MongoDB
        self.collection: AsyncIOMotorCollection = self.db.recipes       # Selecciona la colección de recetas

    async def get_recipe_by_recipe(self, recipe: str):        
        recipe_data = await self.collection.find_one({"recipe": recipe})  # find_one() asíncrono
        
        if recipe_data:
            return Recipe(recipe=recipe_data['recipe'], ingredients=recipe_data['ingredients'])
        return None
    
    async def get_all_recipes(self):
        recipes_cursor = self.collection.find()  # find() asíncrono
        recipes = []
        async for recipe_data in recipes_cursor:  # Usamos 'async for' para iterar de manera asíncrona
            recipes.append(Recipe(recipe=recipe_data['recipe'], ingredients=recipe_data['ingredients']))
        return recipes
