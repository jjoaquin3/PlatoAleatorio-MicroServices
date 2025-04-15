from pydantic import BaseModel
from typing import List
from typing import Optional
from datetime import datetime

class PurchaseSchema(BaseModel):
    ingredient_name: str
    quantity: int
    origin: str
    purchase_date: datetime

class PurchaseRequest(BaseModel):
    order: Optional[int]=None
    ingredient_name: str 

class IngredientSchemaJSON(BaseModel):
    name: str
    state: str
    quantity: int
    pending: int
    send_out: int

class OrderSchemaJSON(BaseModel):
    order: int
    state: str
    recipe: str
    step: str
    created_at: str
    updated_at: str
    ingredients: Optional [List[IngredientSchemaJSON]] = []
