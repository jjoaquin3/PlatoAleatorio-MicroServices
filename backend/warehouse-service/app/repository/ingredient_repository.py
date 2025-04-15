from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.model.ingredient import Ingredient
from app.config.dependencies import get_db_client
from fastapi import Depends

class IngredientRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_client)):
        self.db = db

    async def get_all_ingredients(self):
        result = await self.db.execute(select(Ingredient))
        return result.scalars().all()

    async def get_ingredient_by_name(self, name: str):
        stmt = select(Ingredient).filter_by(name=name)
        result = await self.db.execute(stmt)
        return result.scalars().first()

    async def update_stock_ingredient(self, name: str, quantity: int):
        stmt = select(Ingredient).filter_by(name=name)
        result = await self.db.execute(stmt)
        ingredient = result.scalars().first()
        
        if ingredient:            
            ingredient.quantity += quantity
            await self.db.commit()            
            await self.db.refresh(ingredient)
            return ingredient
        return None
