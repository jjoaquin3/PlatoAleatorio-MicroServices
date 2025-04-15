from fastapi import Depends
from app.repository.purchase_repository import PurchaseRepository
from app.util.external_api import get_quantity_sold
from app.model.purchase import Purchase
from app.model.schema.purchase import PurchaseRequest

class MarketService:
    def __init__(self, purchase_repository: PurchaseRepository = Depends()):
        self.purchase_repository = purchase_repository

    async def get_all_purchases(self):
        return await self.purchase_repository.get_all_purchases()

    async def process_purchase(self, request: PurchaseRequest):
        # Consultar API externa para verificar cantidad disponible
        ingredient_name = request.ingredient_name
        quantity_sold = await get_quantity_sold(ingredient_name)

        # Si la cantidad vendida es mayor que 0, compra exitosa
        if quantity_sold > 0:
            # Registrar la compra exitosa en el historial
            purchase_record = Purchase(ingredient_name=ingredient_name, origin = "process_purchase",  quantity=quantity_sold)
            await self.purchase_repository.save_purchase(purchase_record)        
            
            return {
                "order":request.order,
                "status": "success", 
                "ingredient": ingredient_name, 
                "quantity_sold": quantity_sold,
                "origin":"process_purchase",
                "purchase_date": purchase_record.purchase_date.isoformat()
            }
        
        # Si la cantidad vendida es 0, la compra no se realizó
        return {
            "order":request.order,
            "status": "failure", 
            "ingredient": ingredient_name, 
            "quantity_sold": 0
        }