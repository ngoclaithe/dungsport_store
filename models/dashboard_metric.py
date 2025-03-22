from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP
from models import db

class DashboardMetric(db.Model):
    __tablename__ = 'dashboard_metrics'
    id_metric = Column(Integer, primary_key=True, autoincrement=True)
    metric_name = Column(String(255))
    metric_value = Column(DECIMAL(10, 2))
    record_date = Column(TIMESTAMP)