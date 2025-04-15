import os
import requests
import json
from copy import deepcopy


API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-KEY": API_KEY}

# Puedes mover estas URLs a variables de entorno
KITCHEN_URL = os.getenv("KITCHEN_URL", "http://kitchen-server:8000")
WAREHOUSE_URL = os.getenv("WAREHOUSE_URL", "http://warehouse-server:8000")
MARKET_URL = os.getenv("MARKET_URL", "http://market-server:8000")

class RemoteGateway:

    # ----- KITCHEN -----
    def get_all_recipes(self):
        try:
            response = requests.get(f"{KITCHEN_URL}/recipes", headers=HEADERS)
            return response.json() if response.status_code == 200 else []
        except:
            return []
        
    def get_order(self, order_id: int):
        try:
            response = requests.get(f"{KITCHEN_URL}/orders/{order_id}", headers=HEADERS)
            return response.json() if response.status_code == 200 else None
        except:
            return None
    
    def save_order(self, order_payload: dict, origin:str):
        try:
            response = requests.post(f"{KITCHEN_URL}/orders", headers=HEADERS, json=order_payload)
            if response.status_code != 200:
                print(f"{origin} 🔁 Respuesta:")
                print(response.status_code, response.text)
                print(f"{origin} ⚠️ Error al guardar orden {order_payload.get('order')}")
                return None
        except Exception as e:
            print(f"{origin} 💥 Error en post_order: {e}")
            return None

    def build_order_recipe(self, data: dict):
        try:
            response = requests.post(f"{KITCHEN_URL}/orders/build", headers=HEADERS, json=data)
            print("→ build_order_recipe status:", response.status_code)
            print("→ build_order_recipe response:", response.text)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print("→ build_order_recipe exception:", e)
            return None

    def validate_ingredients(self, data: dict) -> bool:
        try:
            response = requests.post(f"{KITCHEN_URL}/orders/validate", headers=HEADERS, json=data)
            return response.status_code == 200
        except:
            return False

    def update_order_state(self, order: int, state: str):
        payload = {"order": order, "state": state}
        try:
            requests.put(f"{KITCHEN_URL}/orders/state", headers=HEADERS, json=payload)
        except:
            pass

    def update_order_step(self, order: int, step: str):
        payload = {"order": order, "step": step}
        try:
            requests.put(f"{KITCHEN_URL}/orders/step", headers=HEADERS, json=payload)
        except:
            pass

    # ----- WAREHOUSE -----
    def get_ingredients_from_warehouse(self, order_payload: dict):
        try:
            response = requests.post(f"{WAREHOUSE_URL}/ingredients/get_ingredients_by_order",
                                     headers=HEADERS, json=order_payload)
            return response.json() if response.status_code == 200 else None
        except:
            return None
        
    def update_warehouse_stock(self, name: str, quantity: int):
        try:
            payload = {"name": name, "quantity": quantity}
            response = requests.patch(f"{WAREHOUSE_URL}/ingredients", headers=HEADERS, json=payload)
            if response.status_code != 200:
                print(f"⚠️ Falló actualización de warehouse para {name}")
        except Exception as e:
            print(f"💥 Error notificando a warehouse: {e}")

    # ----- MARKET -----
    def purchase_ingredient(self, order: int, ingredient_name: str):
        try:
            payload = {"order": order, "ingredient_name": ingredient_name}
            response = requests.post(f"{MARKET_URL}/market/purchases", headers=HEADERS, json=payload)
            return response.json() if response.status_code == 200 else None
        except:
            return None
