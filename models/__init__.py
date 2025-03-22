from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)
    with app.app_context():
        from models.user import User
        from models.category import Category
        from models.dashboard_metric import DashboardMetric
        from models.inventory_log import InventoryLog
        from models.order import Order
        from models.order_detail import OrderDetail
        from models.payment import Payment
        from models.product import Product
        from models.staff import Staff
        db.create_all()
        print("Database tables created successfully!")