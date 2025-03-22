from sqlalchemy import Column, Integer, String, DECIMAL, Date
from models import db

class Staff(db.Model):
    __tablename__ = 'staff'
    id_staff = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(255))
    email = Column(String(255), unique=True)
    phone = Column(String(15))
    position = Column(String(255))
    salary = Column(DECIMAL(10, 2))
    hire_date = Column(Date)