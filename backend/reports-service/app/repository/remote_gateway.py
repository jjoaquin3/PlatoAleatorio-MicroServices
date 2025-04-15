import os
import httpx

# Variables de entorno
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-KEY": API_KEY}

KITCHEN_URL = os.getenv("KITCHEN_URL", "http://kitchen-server:8000")
WAREHOUSE_URL = os.getenv("WAREHOUSE_URL", "http://warehouse-server:8000")
MARKET_URL = os.getenv("MARKET_URL", "http://market-server:8000")

class RemoteGateway:
    # ----- KITCHEN -----
    async def get_all_orders(self) :
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{KITCHEN_URL}/orders", headers=HEADERS)
                return response.json() if response.status_code == 200 else []
            except Exception as e:
                print(f"Error fetching orders from kitchen: {e}")
                return []

    async def get_recipes(self) :
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{KITCHEN_URL}/recipes", headers=HEADERS)
                return response.json() if response.status_code == 200 else []
            except Exception as e:
                print(f"Error fetching recipes from kitchen: {e}")
                return []

    async def get_next_order_id(self) :
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(f"{KITCHEN_URL}/orders/next-id", headers=HEADERS)
                return response.json() if response.status_code == 200 else {}
            except Exception as e:
                print(f"Error fetching next order ID from kitchen: {e}")
                return {}

    # ----- WAREHOUSE -----
    async def get_all_ingredients(self):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{WAREHOUSE_URL}/ingredients", headers=HEADERS)
                return response.json() if response.status_code == 200 else []
            except Exception as e:
                print(f"Error fetching ingredients from warehouse: {e}")
                return []

    # ----- MARKET -----
    async def get_all_purchases(self) :
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{MARKET_URL}/market/purchases", headers=HEADERS)
                return response.json() if response.status_code == 200 else []
            except Exception as e:
                print(f"Error fetching purchases from market: {e}")
                return []
