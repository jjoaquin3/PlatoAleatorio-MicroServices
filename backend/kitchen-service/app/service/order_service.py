from app.repository.order_repository import OrderRepository
from app.repository.recipe_repository import RecipeRepository
from app.service.recipe_service import RecipeService
from datetime import datetime
from fastapi import Depends
from app.model.schema.order import OrderUpdateStateRequest, OrderUpdateStepRequest, OrderSchemaBuild, OrderSchema
from datetime import datetime
from app.model.schema.order import IngredientSchema

class OrderService:
    def __init__(
            self, order_repository: OrderRepository = Depends(), 
            recipe_service: RecipeService = Depends()
        ):
        self.order_repository = order_repository
        self.recipe_service = recipe_service

    async def  get_all_orders(self):
        return await self.order_repository.get_all_orders()

    async def  get_order_by_order(self, order_number: int):        
        return await self.order_repository.get_order_by_order(order_number)

    async def  update_step(self, request: OrderUpdateStepRequest):        
        return await self.order_repository.update_step(request.order, request.step)

    async def  update_state(self, request: OrderUpdateStateRequest):        
        return await self.order_repository.update_state(request.order, request.state)

    async def  save_order(self, order_data: dict):
        print("save order 1 en service")
        print(f"Payload a guardar: {order_data}")  # Log del payload antes de guardar la orden        
        return await self.order_repository.save_order(order_data.dict())
    
    async def build_order_recipe(self, order_data: OrderSchemaBuild):        
        recipe_name = order_data.recipe
        recipe = await self.recipe_service.get_recipe_by_recipe(recipe_name)
        
        # Crear una instancia de OrderSchema
        result = OrderSchema(
            order=order_data.order,
            recipe=order_data.recipe,
            state="pending",  # Esto ya lo asignamos directamente
            step="kitchen",   # Lo mismo aquí
            created_at=int(datetime.utcnow().timestamp()),
            updated_at=int(datetime.utcnow().timestamp())
        )

        if recipe:
            # Construir el JSON de la orden con los ingredientes de la receta
            result.ingredients = [IngredientSchema(**ingredient) for ingredient in recipe.ingredients]            

            # Guarda la orden en la DB
            print("Saver order 1")
            saved = await self.order_repository.save_order(result.dict())  # Ahora podemos usar dict() porque 'result' es una instancia
            print(f"Saver order 2 {saved}")
            
            return result if saved else None        
        
        return None  # Si no se encuentra la receta, devolver None
    
    async def validate_ingredients(self, order_data: dict) -> bool:
        # Verifica que todos los ingredientes 
        # tengan el ingredientestate = 'complete'
        # ingrediente.pending se 0, es decir no falta ingredientes
        # ingrediente.send_out sea igua a la cantidad que dice la receta ingrediente.quantity
        for ingredient in order_data["ingredients"]:
            if not (ingredient["state"] == "complete" and ingredient["pending"] == 0 and ingredient["quantity"] == ingredient["send_out"]):
                return False  # Si algún ingrediente no cumple, devuelve False
        return True