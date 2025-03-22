from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from models import db

class Brand(db.Model):
    __tablename__ = 'brands'
    id_brand = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String(255), nullable=False)
    description = Column(Text)
    created_at = Column(TIMESTAMP)
