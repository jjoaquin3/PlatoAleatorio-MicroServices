from datetime import datetime
from typing import List
from app.config.date_zone import DateZone

class Ingredient:
    def __init__(self, name: str, state: str, quantity: int, pending: int, send_out: int):
        self.name = name
        self.state = state
        self.quantity = quantity
        self.pending = pending
        self.send_out = send_out

class Order:
    def __init__(self, order: int, state: str, recipe: str, step: str, ingredients: List[Ingredient], created_at: int = None, updated_at: int = None):
        self.order = order
        self.state = state
        self.recipe = recipe
        self.step = step
        self.ingredients = ingredients
        self.created_at = created_at or DateZone.get_current_time()  # Cambiar de datetime a int
        self.updated_at = updated_at or DateZone.get_current_time()  # Cambiar de datetime a int