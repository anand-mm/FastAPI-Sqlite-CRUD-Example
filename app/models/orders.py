from sqlalchemy import Column, Integer, String
from app.db import Base

class Item(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_name = Column(String, index=True)
    order_description = Column(String, index=True)