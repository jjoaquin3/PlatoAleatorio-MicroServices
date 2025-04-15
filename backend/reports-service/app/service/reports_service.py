from app.repository.remote_gateway import RemoteGateway
#from app.model.schema.order import OrderSchema, PurchaseSchema, IngredientSchema, RecipeSchema
from typing import List
from fastapi import Depends

class ReportsService:
    def __init__(self, remote_gateway: RemoteGateway = Depends()):
        self.remote_gateway = remote_gateway

    async def get_orders(self) :
        return await self.remote_gateway.get_all_orders()

    async def get_ingredients(self)  :
        return await self.remote_gateway.get_all_ingredients()

    async def get_recipes(self)  :
        return await self.remote_gateway.get_recipes()

    async def get_market_purchases(self) :
        return await self.remote_gateway.get_all_purchases()

    async def get_next_order_id(self) :
        return await self.remote_gateway.get_next_order_id()
