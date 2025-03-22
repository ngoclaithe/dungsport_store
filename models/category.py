from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from models import db

class Category(db.Model):
    __tablename__ = 'categories'
    id_category = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(255))
    description = Column(Text)
    created_at = Column(TIMESTAMP)