from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from app.config.date_zone import DateZone
from sqlalchemy.sql import func
import os

Base = declarative_base()
SCHEMA = os.getenv("POSTGRES_SCHEMA_MARKET")

class Purchase(Base):
    __tablename__ = 'purchases'
    __table_args__ = {'schema': SCHEMA} 

    id = Column(Integer, primary_key=True, autoincrement=True)
    ingredient_name = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    origin = Column(String(32), nullable=False)
    purchase_date = Column(DateTime(timezone=True), server_default=func.now())
    def __repr__(self):
        return f"<Purchase(id={self.id}, ingredient_name={self.ingredient_name}, quantity={self.quantity}, origin={self.origin}, purchase_date={self.purchase_date})>"
