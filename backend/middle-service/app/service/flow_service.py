import random
import requests
from app.config.redis_client import RedisClient
from app.model.schema.order import OrderSchemaBuild
from app.repository.remote_gateway import RemoteGateway
import json
from app.config.date_zone import DateZone
from datetime import datetime

class FlowService:

    def __init__(self):        
        self.redis = RedisClient.get_client()
        self.gateway = RemoteGateway()
        print("fs 🔗 Redis conectado:", self.redis.ping())

    async def handle_order_request(self, order_data: dict) -> dict:
        order_id = order_data["order"]
        print(f"0. handle_order_request de {order_id}")

        # 1. Obtener recetas disponibles
        print("1. Obtener recetas disponibles")
        recipes = self.gateway.get_all_recipes()  # GET /recipes
        if not recipes:
            return {"error": "No recipes available"}

        # 2. Elegir receta al azar
        print("2. Elegir receta al azar")
        selected_recipe = random.choice(recipes)
        recipe_name = selected_recipe["recipe"]

        # 3. Construir orden en cocina
        print("3. Construir orden en cocina")
        build_data = {
            "order": order_id,
            "state": "process",
            "recipe": recipe_name
        }
        build_response = self.gateway.build_order_recipe(build_data)  # POST /orders/build
        if not build_response:
            return {"error": "Failed to build order"}
    
        # 4. Pedir ingredientes a warehouse
        print("4. Pedir ingredientes a warehouse")
        warehouse_response = self.gateway.get_ingredients_from_warehouse(build_response)
        if not warehouse_response:
            return {"error": "Warehouse failed to respond"}
        
        # 5. Actualizar orden después de que el warehouse despache ingredientes
        print("5. Actualizar orden después de que el warehouse despache ingredientes")
        #self.save_order(warehouse_response, "FlowService handle")
        #self.gateway.update_order_step(order_id, "kitchen")

        # 6. Validar con cocina
        print("6. Validar con cocina")
        validation_ok = self.gateway.validate_ingredients(warehouse_response)
        print(f"🔍 Resultado de validación para orden {order_id}: {validation_ok}")

        if validation_ok:
            print("6.2 Validar con cocina bien se entrega platillo")
            self.save_order(warehouse_response, "FlowService handle")
            self.gateway.update_order_state(order_id, "complete")
            self.gateway.update_order_step(order_id, "delivery")
            self.cleanup_queues(order_id)
            return {"message": "Order completed", "order": order_id, "recipe":warehouse_response["recipe"]}

        # Si no se completó, loggear y encolar ingredientes pendientes
        print("6.1 Validar con cocina fallida se encola")
        self.save_order(warehouse_response, "FlowService handle")
        print(f"⚠️ Orden {order_id} incompleta, intentando encolar ingredientes pendientes...")
        print("📦 Respuesta de warehouse:")
        print(json.dumps(warehouse_response, indent=2))

        for ingredient in warehouse_response["ingredients"]:
            if ingredient["state"] == "pending":
                payload = {
                    "order": order_id,
                    "ingredient_name": ingredient["name"]
                }
                print(f"🛒 Encolando compra para orden {order_id}: {ingredient['name']}")
                self.redis.rpush("market_queue", json.dumps(payload))
                print("✅ Encolado")

        self.gateway.update_order_step(order_id, "market")        
        #return {"message": "Order waiting for ingredients", "order": order_id}
        return {"message": "Order waiting for ingredients", "order": order_id, "recipe":warehouse_response["recipe"]}


    def cleanup_queues(self, order_id: int):
        # Si usás claves por orden tipo market_queue:{order}
        self.redis.delete(f"market_queue:{order_id}")
        self.redis.delete(f"market_retry_queue:{order_id}")

    def save_order(self, updated_order: dict, origin:str):
        print(f"qw A0. Save Order by {origin}")
        print("fs A1. flow save order ")
        order_id = updated_order.get("order")
        current = self.gateway.get_order(order_id)
        if not current:
            print(f"⚠️ No se pudo obtener orden {order_id}")
            return

        print("fs A2. flow save order ")
        current_ingredients = {i["name"]: i for i in current.get("ingredients", [])}
        new_data = {i["name"]: i for i in updated_order.get("ingredients", [])}

        for name, updates in new_data.items():
            current_ingredients[name].update(updates)

        print("fs A3. flow save order ")        
        current["ingredients"] = list(current_ingredients.values())
        current["state"]= updated_order.get("state")
        current["step"]= updated_order.get("step")
        current["updated_at"]= updated_order.get("updated_at")

        # Convertir las fechas a Unix timestamps si no están presentes
        # Convertir las fechas a Unix timestamps si no están presentes
        #if isinstance(current.get("created_at"), datetime):
        #    current["created_at"] = int(current["created_at"].timestamp())  # Convertir datetime a Unix timestamp
        #elif isinstance(current.get("created_at"), int):
        #    pass  # Ya es un Unix timestamp, no necesitamos hacer nada

        # Actualizar `updated_at` a Unix timestamp
        print("fs A4. flow save order ")
        #current["updated_at"] = int(DateZone.get_current_time())  # Siempre actualizamos `updated_at`

        print("fs 📤 Payload final a guardar:")
        print(json.dumps(current, indent=2))
        print("fs A5. flow save order ")
        self.gateway.save_order(current, origin)  # Guardamos la orden actualizada