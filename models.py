from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Item(Base):
    __tablename__ = "items"  # ✅ Correct way to define table name
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
