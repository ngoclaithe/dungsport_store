from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from models import db
from models.brand import Brand

class Product(db.Model):
    __tablename__ = 'products'
    id_product = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    id_category = Column(Integer, ForeignKey('categories.id_category'), nullable=True)
    id_brand = Column(Integer, ForeignKey('brands.id_brand'), nullable=True)
    
    price = Column(DECIMAL(10, 2))
    cost_price = Column(DECIMAL(10, 2))
    inventory = Column(Integer)
    description = Column(Text)
    created_at = Column(TIMESTAMP, server_default=func.now())  
    size = Column(String(50), nullable=True)            
    color = Column(String(50), nullable=True)  
    
    discount = Column(Integer, nullable=True, default="0")
    
    category = relationship("Category", backref="products")
    brand = relationship("Brand", backref="products")
