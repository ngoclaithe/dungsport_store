from sqlalchemy import Column, Integer, DECIMAL, ForeignKey
from models import db

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    
    id_product = Column(Integer, ForeignKey('products.id_product'))
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    original_price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    color = db.Column(db.String(50))
    size = db.Column(db.String(50))
    brand = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<OrderDetail {self.name} x {self.quantity}>'
