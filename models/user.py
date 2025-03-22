from models import db
from sqlalchemy import Column, Integer, String, Text, Enum, TIMESTAMP

class User(db.Model):
    __tablename__ = 'users'
    
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    fullname = Column(String(255))
    email = Column(String(255), unique=True)
    password_hash = Column(String(255))
    phone = Column(String(15))
    province = Column(Text)
    district = Column(Text)
    address = Column(Text)
    ward = Column(Text)
    role = Column(Enum('customer', 'admin', 'staff'))
    
    def __repr__(self):
        return f"<User {self.username}>"
