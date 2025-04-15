from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()
SCHEMA = os.getenv("POSTGRES_SCHEMA_WAREHOUSE")

class Ingredient(Base):
    __tablename__ = 'ingredients'
    __table_args__ = {'schema': SCHEMA} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), unique=True, nullable=False)
    quantity = Column(Integer, nullable=False, default=5)

    def __repr__(self):
        return f"<Ingredient(name={self.name}, quantity={self.quantity})>"
