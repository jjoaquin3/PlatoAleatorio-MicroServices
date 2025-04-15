from fastapi import Depends
from app.repository.ingredient_repository import IngredientRepository
from app.model.schema.ingredient import OrderSchemaJSON
from typing import List

class IngredientService:
    def __init__(self, ingredient_repository: IngredientRepository = Depends()):
        self.ingredient_repository = ingredient_repository

    async def get_all_ingredients(self):
        return await self.ingredient_repository.get_all_ingredients()

    async def get_ingredient_by_name(self, name: str):
        return await self.ingredient_repository.get_ingredient_by_name(name)

    async def update_stock_ingredient(self, name: str, quantity: int):
        return await self.ingredient_repository.update_stock_ingredient(name, quantity)

    async def get_ingredients_by_order(self, order_data: OrderSchemaJSON):
        updated_ingredients = []

        for ingredient_data in order_data.ingredients:
            
            if ingredient_data.state == 'complete':
                continue

            ingredient_name = ingredient_data.name
            ingredient = await self.ingredient_repository.get_ingredient_by_name(ingredient_name)

            if ingredient:
                available_quantity = ingredient.quantity  # Lo que hay en bodega
                additional_send_out = 0

                # Si hay suficiente stock para satisfacer la solicitud
                if available_quantity >= ingredient_data.pending:
                    additional_send_out = ingredient_data.pending
                    ingredient_data.state = "complete"
                    ingredient_data.pending = 0
                    ingredient_data.send_out += additional_send_out  # Sumar la cantidad que se despacha
                elif available_quantity > 0:       
                    # Si hay algunos ingredientes disponibles pero no suficientes
                    additional_send_out = available_quantity
                    ingredient_data.state = "pending"
                    ingredient_data.pending -= additional_send_out  # Reducir lo que falta por despachar
                    ingredient_data.send_out += additional_send_out  # Sumar la cantidad que se despacha
                # Si no hay suficiente stock, no hacemos nada, solo se pasa al siguiente ingrediente                   
                 
                # Actualizamos el ingrediente en la base de datos solo si se hizo un despacho
                if additional_send_out > 0:
                    await self.ingredient_repository.update_stock_ingredient(
                        ingredient_name, additional_send_out * (-1)
                    )

                updated_ingredients.append(ingredient_data)

            else:
                # Si no existe el ingrediente, lo agregamos tal como está
                updated_ingredients.append(ingredient_data)

        # Determinar el estado de la solicitud (pending o complete)
        if all(ingredient.state == 'complete' for ingredient in updated_ingredients):
            order_data.state = "complete"
            order_data.step = "warehouse"
        else:
            order_data.state ="pending"
            order_data.step = "warehouse"

        # Actualizamos el resto de los datos de la orden
        order_data.ingredients = updated_ingredients
        return order_data