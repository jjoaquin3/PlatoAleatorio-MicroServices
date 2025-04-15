import aiohttp
import asyncio

async def get_quantity_sold(ingredient_name: str) -> int:
    url = f"https://recruitment.alegra.com/api/farmers-market/buy?ingredient={ingredient_name.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data.get("quantitySold", 0)
