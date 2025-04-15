from app.config.dependencies import get_mongo_client
from motor.motor_asyncio import AsyncIOMotorCollection  # Usamos Motor en lugar de pymongo
from datetime import datetime
from app.model.order import Order, Ingredient
from app.model.schema.order import OrderSchema
from typing import Optional, List
from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorClient

class OrderRepository:
    def __init__(self, mongo_client: AsyncIOMotorClient = Depends(get_mongo_client)):
        self.db = mongo_client
        self.collection: AsyncIOMotorCollection = self.db.orders  # Usar colección asíncrona

    async def get_all_orders(self) -> List[Order]:
        # Recupera todas las órdenes de forma asíncrona
        orders_data = self.collection.find()  # find() es asíncrono con Motor
        orders = []
        async for order_data in orders_data:  # Usamos 'async for' para iterar de manera asíncrona
            ingredients = [Ingredient(**ingredient) for ingredient in order_data["ingredients"]]
            orders.append(Order(
                order=order_data["order"],
                state=order_data["state"],
                recipe=order_data["recipe"],
                step=order_data["step"],
                ingredients=ingredients,
                created_at=order_data["created_at"],
                updated_at=order_data["updated_at"]
            ))
        return orders

    async def get_order_by_order(self, order_number: int) -> Optional[Order]:
        # Buscar la orden por el número de la orden de forma asíncrona
        order_data = await self.collection.find_one({"order": order_number})  # find_one() asíncrono
        if order_data:
            ingredients = [Ingredient(**ingredient) for ingredient in order_data["ingredients"]]
            return Order(
                order=order_data["order"],
                state=order_data["state"],
                recipe=order_data["recipe"],
                step=order_data["step"],
                ingredients=ingredients,
                created_at=order_data["created_at"],
                updated_at=order_data["updated_at"]
            )
        return None

    async def update_step(self, order_number: int, new_step: str) -> bool:
        # Actualiza el campo 'step' de la orden de forma asíncrona
        result = await self.collection.update_one(
            {"order": order_number},
            {"$set": {"step": new_step, "updated_at": int(datetime.utcnow().timestamp())}}
        )
        return result.modified_count > 0  # Retorna True si se actualizó, False si no

    async def update_state(self, order_number: int, new_state: str) -> bool:
        # Actualiza el campo 'state' de la orden de forma asíncrona
        result = await self.collection.update_one(
            {"order": order_number},
            {"$set": {"state": new_state, "updated_at": int(datetime.utcnow().timestamp())}}
        )
        return result.modified_count > 0  # Retorna True si se actualizó, False si no

    async def save_order(self, order_data: dict) -> bool:
        # Guarda o actualiza la orden de forma asíncrona
        current_timestamp = int(datetime.utcnow().timestamp())
        existing_order = await self.collection.find_one({"order": order_data["order"]})  # find_one() asíncrono
        if existing_order:
            # Si ya existe la orden, actualizamos
            result = await self.collection.update_one(
                {"order": order_data["order"]},
                {"$set": order_data}
            )
            return result.modified_count > 0  # Retorna True si se actualizó
        else:
            # Si no existe, insertamos la nueva orden
            result = await self.collection.insert_one(order_data)
            return result.inserted_id is not None
