from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, Enum
from models import db

class Payment(db.Model):
    __tablename__ = 'payments'
    id_payment = Column(Integer, primary_key=True, autoincrement=True)
    id_order = Column(Integer,nullable=False)
    payment_method = Column(String(255))
    payment_date = Column(DateTime)
    amount = Column(DECIMAL(10, 2))
    status = Column(Enum('paid', 'unpaid', 'refunded'))