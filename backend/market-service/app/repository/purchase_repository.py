from app.config.dependencies import get_db_client
from app.model.purchase import Purchase
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends

class PurchaseRepository:
    def __init__(self, db: AsyncSession = Depends(get_db_client)):
        self.db = db
        
    async def save_purchase(self, purchase: Purchase):        
        self.db.add(purchase)
        await self.db.commit()   
        await self.db.refresh(purchase)  
        return purchase
    
    async def get_all_purchases(self):
        result = await self.db.execute(select(Purchase))
        return result.scalars().all()