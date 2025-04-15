from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# DB tiene id, name, quantity
class IngredientSchema(BaseModel):
    name: str
    quantity: int

    class Config:
        exclude = {"id"}

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
    created_at: Optional[int] = None
    updated_at: Optional[int] = None
    ingredients: List[IngredientSchemaJSON]