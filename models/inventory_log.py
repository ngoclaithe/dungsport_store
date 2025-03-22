from sqlalchemy import Column, Integer, Text, TIMESTAMP, Enum, ForeignKey
from models import db

class InventoryLog(db.Model):
    __tablename__ = 'inventory_log'
    id_log = Column(Integer, primary_key=True, autoincrement=True)
    id_product = Column(Integer, ForeignKey('products.id_product'))
    change_quantity = Column(Integer)
    change_type = Column(Enum('import', 'export', 'adjustment'))
    log_date = Column(TIMESTAMP)
    note = Column(Text)