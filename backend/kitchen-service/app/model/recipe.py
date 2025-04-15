from pymongo import MongoClient
from bson import ObjectId
from typing import List

class Ingredient:
    def __init__(self, name: str, state: str, quantity: int, pending: int, send_out: int):
        self.name = name
        self.state = state
        self.quantity = quantity
        self.pending = pending
        self.send_out = send_out

class Recipe:
    def __init__(self, recipe: str, ingredients: List[Ingredient]):
        self.recipe = recipe
        self.ingredients = ingredients

    def to_dict(self):
        return {
            "recipe": self.recipe,
            "ingredients": [ingredient.__dict__ for ingredient in self.ingredients]
        }
