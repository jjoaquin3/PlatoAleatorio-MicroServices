import time
import json
from app.config.redis_client import RedisClient
from app.repository.remote_gateway import RemoteGateway
from app.config.date_zone import DateZone
from datetime import datetime

class QueueWorker:

    def __init__(self):
        self.redis = RedisClient.get_client()
        self.gateway = RemoteGateway()

    def run_market_queue(self):
        print("rmq 📦 Worker de market_queue iniciado")
        while True:
            item = self.redis.lpop("market_queue")
            if item:
                print("rmq 📦 Item encontrado:", item)
                
                try:
                    data = json.loads(item)
                    order_id = data["order"]
                    ingredient_name = data["ingredient_name"]

                    print(f"rmq 1. Comprando: {ingredient_name} para orden {order_id}")
                    result = self.gateway.purchase_ingredient(order_id, ingredient_name)

                    if result and result.get("status") == "success":
                        # 2. Esperar compra exitosa
                        print(f"rmq 1. Compra exitosa: {ingredient_name}")

                        # 2. Actualizar stock en warehouse
                        print("rmq 2. Actualizar stock en warehouse")
                        self.gateway.update_warehouse_stock(ingredient_name, result.get("quantity_sold"))

                        # 3. Obtener la orden como está en mongo
                        print("rmq 3. Obtener la orden como está en mongo")
                        current_order = self.gateway.get_order(order_id)
                        if not current_order:
                            print("rmq 3.1. No se pudo obtener la orden para validar")
                            continue
                        
                        # 4. Pedir ingredientes a warehouse
                        print("rmq 4. Pedir ingredientes a warehouse")
                        #self.gateway.update_order_step(order_id, "warehouse") 
                        updated_order = self.gateway.get_ingredients_from_warehouse(current_order)
                        if not updated_order:
                            print("rmq 4.1. Falló warehouse al actualizar")
                            continue

                        # 5. Actualizar orden después de que el warehouse despache ingredientes
                        print("rmq 5. Actualizar orden después de que el warehouse despache ingredientes")                                                
                        #self.save_order(updated_order, "rmq l54")                        

                        # 6. Validar con cocina
                        print("rmq 6. Validar con cocina")
                        validation_ok = self.gateway.validate_ingredients(updated_order)
                        print(f"rmq 6.1. Resultado de validación para orden {order_id}: {validation_ok}")                        

                        if validation_ok:          
                            updated_order["step"] ="delivery"
                            updated_order["state"] ="complete"
                            self.save_order(updated_order, "rmq 64")         
                            self.clean_order_from_queue(order_id)                                                                       
                            print(f"rmq 6.2. Orden {order_id} completada ✅")
                        else:
                            print(f"rmq 6.3. Orden {order_id} sigue pendiente")      
                            updated_order["step"] ="market q1"
                            updated_order["state"] ="pending"
                            self.save_order(updated_order, "rmq 71") 

                            for ingredient in updated_order.get("ingredients", []):
                                if ingredient.get("state") == "pending":
                                    payload = {
                                        "order": order_id,
                                        "ingredient_name": ingredient["name"]
                                    }
                                    print(f"rmq 6.4. Reencolando: {ingredient['name']}")
                                    self.redis.rpush("market_queue", json.dumps(payload))
                                    print("rmq 6.5. ReEncolado")
                    else:
                        print(f"rmq ❌ Compra fallida: {ingredient_name}, reintentando luego")
                        self.redis.rpush("market_retry_queue", json.dumps(data))

                except Exception as e:
                    print("rmq 💥 Error procesando item:", e)
            else:
                time.sleep(1)  # nada en la cola, esperar un poco

    def run_market_retry_queue(self):
        print("rmrq 🔁 Worker de market_retry_queue iniciado")
        while True:
            item = self.redis.lpop("market_retry_queue")
            if item:
                try:
                    data = json.loads(item)
                    order_id = data["order"]
                    ingredient_name = data["ingredient_name"]

                    print(f"rmrq 🔄 Reintentando compra: {ingredient_name} para orden {order_id}")
                    result = self.gateway.purchase_ingredient(order_id, ingredient_name)

                    if result and result.get("status") == "success":
                        # 1. Esperar compra exitosa
                        print(f"rmrq 1. Compra exitosa: {ingredient_name}")
                        print(f"rmrq ✅ Reintento exitoso: {ingredient_name}")

                        # 2. Actualizar stock en warehouse
                        print("rmrq 2. Actualizar stock en warehouse")
                        self.gateway.update_warehouse_stock(ingredient_name, result.get("quantity_sold"))

                        # 3. Obtener la orden como está en mongo
                        print("rmrq 3. Obtener la orden como está en mongo")
                        current_order = self.gateway.get_order(order_id)
                        if not current_order:
                            print("rmrq 3.1. No se pudo obtener la orden para validar")
                            continue

                        # 4. Pedir ingredientes a warehouse
                        print("rmrq 4. Pedir ingredientes a warehouse")
                        #self.gateway.update_order_step(order_id, "warehouse")  
                        updated_order = self.gateway.get_ingredients_from_warehouse(current_order)
                        if not updated_order:
                            print("rmrq ⚠️ Falló warehouse al actualizar")
                            continue
                        
                        # 5. Actualizar orden después de que el warehouse despache ingredientes
                        print("rmrq 5. Actualizar orden después de que el warehouse despache ingredientes")                        
                        #self.gateway.update_order_state(order_id, "kitchen")
                        #updated_order["step"] = "warehouse"
                        #updated_order["updated_at"] = int(DateZone.get_current_time())
                        #self.save_order(updated_order, "rmq l129")     

                        # 6. Validar con cocina
                        print("rmrq 6. Validar con cocina")
                        validation_ok = self.gateway.validate_ingredients(updated_order)
                        print(f"rmrq 6.1. Resultado de validación para orden {order_id}: {validation_ok}")

                        if validation_ok:                                                                     
                            updated_order["step"] ="delivery"
                            updated_order["state"] ="complete"
                            self.save_order(updated_order, "rmq 143")         
                            self.clean_order_from_queue(order_id)   
                            #self.gateway.update_order_state(order_id, "complete")                            
                            #self.gateway.update_order_step(order_id, "delivery")                                                                                 
                            print(f"rmrq 6.2. Orden {order_id} completada desde retry ✅")
                        else:
                            print(f"rmrq 6.3. Orden {order_id} sigue pendiente después del reintento")
                            updated_order["step"] ="market q2"
                            updated_order["state"] ="pending"
                            self.save_order(updated_order, "rmq 152")         
                            #self.gateway.update_order_step(order_id, "market queue 2")
                            # 2. Reencolar lo que aún falta
                            for ingredient in updated_order.get("ingredients", []):
                                if ingredient.get("state") == "pending":
                                    payload = {
                                        "order": order_id,
                                        "ingredient_name": ingredient["name"]
                                    }
                                    print(f"rmrq 6.4 Reencolando: {ingredient['name']}")
                                    self.redis.rpush("market_queue", json.dumps(payload))     
                                    print("rmq 6.5. ReEncolado")                   
                    else:
                        print(f"rmrq ⏳ Ingrediente aún no disponible: {ingredient_name}, reencolando")
                        time.sleep(5)  # delay antes de reencolar
                        self.redis.rpush("market_retry_queue", json.dumps(data))

                except Exception as e:
                    print("rmrq 💥 Error en retry:", e)
            else:
                time.sleep(2)

    def clean_order_from_queue(self, order_id: int):
        print(f"🧹 Limpiando colas para orden {order_id}...")

        for queue_name in ["market_queue", "market_retry_queue"]:
            temp_items = []
            queue_len = self.redis.llen(queue_name)

            for _ in range(queue_len):
                item = self.redis.lpop(queue_name)
                if not item:
                    continue
                try:
                    data = json.loads(item)
                    if data.get("order") != order_id:
                        temp_items.append(item)
                    else:
                        print(f"🗑️ Eliminado de {queue_name}: {data}")
                except:
                    temp_items.append(item)  # evitar perder items corruptos

            # Volver a insertar los que no son de la orden eliminada
            for item in temp_items:
                self.redis.rpush(queue_name, item)

        print(f"✅ Colas limpiadas para orden {order_id}")

    def save_order(self, updated_order: dict, origin:str):
        print(f"qw A0. Save Order by {origin}")
        print(f"qw A0. Payload a guardar: {updated_order}")

        print("qw A1. flow save order")
        order_id = updated_order.get("order")
        current = self.gateway.get_order(order_id)
        if not current:
            print(f"qw ⚠️ No se pudo obtener orden {order_id}")
            return

        print("qw A2. flow save order")
        current_ingredients = {i["name"]: i for i in current.get("ingredients", [])}
        new_data = {i["name"]: i for i in updated_order.get("ingredients", [])}

        for name, updates in new_data.items():
            current_ingredients[name].update(updates)

        print("qw A3. flow save order")
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
        print("qw A4. flow save order")
        #current["updated_at"] = int(DateZone.get_current_time())  # Siempre actualizamos `updated_at`

        print(f"📤 Payload final a guardar: {origin}")
        print(json.dumps(current, indent=2))
        print(f"qw A5. flow save order:  {origin}")
        self.gateway.save_order(current, origin)  # Guardamos la orden actualizada
