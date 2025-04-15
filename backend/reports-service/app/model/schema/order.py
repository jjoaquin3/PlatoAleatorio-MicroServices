from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

   
class IngredientSchemaSimple(BaseModel):
    name: str
    quantity: int

class IngredientSchema(BaseModel):
    name: str
    state: str
    quantity: int
    pending: int
    send_out: int

class RecipeSchema(BaseModel):
    recipe: str
    ingredients: List[IngredientSchema]

class OrderSchema(BaseModel):
    order: int
    state: str
    recipe: str
    step: str
    created_at: Optional[int] = None  
    updated_at: Optional[int] = None  
    ingredients: List[IngredientSchema]

    class Config:
        exclude = {"_id"}

class PurchaseSchema(BaseModel):
    ingredient_name: str
    quantity: int
    origin: str
    purchase_date: datetime

    class Config:
        exclude = {"id"}


