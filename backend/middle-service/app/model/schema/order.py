from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class IngredientSchema(BaseModel):
    name: str
    state: str
    quantity: int
    pending: int
    send_out: int

class OrderSchemaBuild(BaseModel):
    order: int
    state: Optional[str]=None
    recipe: Optional[str]=None    

class OrderUpdateStateRequest(BaseModel):
    order: int
    state: str

class OrderUpdateStepRequest(BaseModel):
    order: int
    step: str

class OrderSchema(BaseModel):
    order: int
    state: str
    recipe: str
    step: str
    created_at: Optional[int] = None  # Cambiar de datetime a int
    updated_at: Optional[int] = None  # Cambiar de datetime a int
    ingredients: List[IngredientSchema]

    class Config:
        exclude = {"_id"}
