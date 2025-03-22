from datetime import datetime
from models import db
from sqlalchemy import Enum

class Order(db.Model):
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.String(20), unique=True, nullable=False)  
    
    customer_fullname = db.Column(db.String(255), nullable=False)
    customer_email = db.Column(db.String(255), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_province = db.Column(db.String(100), nullable=False)
    customer_district = db.Column(db.String(100), nullable=False)
    customer_ward = db.Column(db.String(100), nullable=False)
    customer_address_detail = db.Column(db.String(255), nullable=False)
    
    payment_method = db.Column(db.String(50), nullable=False)
    note = db.Column(db.Text)
    subtotal = db.Column(db.Float, nullable=False)
    shipping_fee = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
    order_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    status = db.Column(Enum('pending', 'approved', 'refused'), default='pending', nullable=False)
    
    order_details = db.relationship('OrderDetail', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.order_id}>'
