from sqlalchemy import Column, Integer, String, Text, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from models import db

class ProductImage(db.Model):
    __tablename__ = 'product_images'
    id_image = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('products.id_product'), nullable=False)
    image_url = Column(String(255), nullable=False)  

    product = relationship("Product", backref="images")