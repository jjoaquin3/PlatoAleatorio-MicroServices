from pydantic import BaseModel
from typing import List

class IngredientSchema(BaseModel):
    name: str
    state: str
    quantity: int
    pending: int
    send_out: int

class RecipeSchema(BaseModel):
    recipe: str
    ingredients: List[IngredientSchema]

    class Config:
        exclude = {"_id"}
