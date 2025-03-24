from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db  
from models.product import Product
from models.order import Order
from models.user import User
from sqlalchemy import func, extract
from datetime import datetime, timedelta
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import random
import json

dashboard_bp = Blueprint("dashboard", __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Bạn cần đăng nhập để vào trang admin!")
            return redirect(url_for("dashboard.login"))
        user = User.query.get(session['user_id'])
        if not user or user.role != "admin":
            flash("Bạn không có quyền truy cập trang admin!")
            return redirect(url_for("dashboard.login"))
        return f(*args, **kwargs)
    return decorated_function

@dashboard_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            if user.role != "admin":
                flash("Tài khoản không có quyền truy cập admin!")
                return redirect(url_for("dashboard.login"))
            session["user_id"] = user.id_user
            return redirect(url_for("dashboard.dashboard"))
        else:
            flash("Tên đăng nhập hoặc mật khẩu không đúng!")
    return render_template("admin/login.html")

def get_monthly_sales_data():
    months = ["T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10", "T11", "T12"]
    current_month = datetime.now().month
    
    sales_data = []
    for i in range(12):
        if i < current_month:
            sales = random.randint(100, 150) * (0.7 + (i / 12))
        else:
            sales = random.randint(80, 120) * (0.5 + (i / 24))
        sales_data.append(int(sales))
    
    return {"labels": months, "data": sales_data}

def get_category_sales():
    categories = ["Giày thể thao", "Quần áo tập gym", "Đồ bơi", "Phụ kiện", "Dụng cụ thể thao"]
    sales = [random.randint(200, 500) for _ in range(len(categories))]
    return {"categories": categories, "sales": sales}

def get_top_products():
    products = [
        {"name": "Giày Nike Air Max", "sales": random.randint(80, 150)},
        {"name": "Áo thun Adidas", "sales": random.randint(70, 140)},
        {"name": "Quần short Under Armour", "sales": random.randint(60, 130)},
        {"name": "Bộ tập Gym Puma", "sales": random.randint(50, 120)},
        {"name": "Vớ thể thao Nike", "sales": random.randint(40, 110)}
    ]
    return sorted(products, key=lambda x: x["sales"], reverse=True)

@dashboard_bp.route("/dashboard")
@admin_required
def dashboard():
    total_products = db.session.query(Product).count()
    total_orders = db.session.query(Order).count()
    total_users = db.session.query(User).count()
    
    total_revenue = random.randint(2500, 5000) * 100000  
    current_month_revenue = random.randint(250, 450) * 100000
    previous_month_revenue = random.randint(200, 400) * 100000
    revenue_growth = ((current_month_revenue - previous_month_revenue) / previous_month_revenue) * 100
    
    new_users_count = random.randint(20, 50)
    user_growth = (new_users_count / total_users) * 100 if total_users > 0 else 0
    
    monthly_sales = get_monthly_sales_data()
    
    category_sales = get_category_sales()
    
    top_products = get_top_products()
    
    formatted_total_revenue = f"{total_revenue:,}".replace(",", ".")
    formatted_month_revenue = f"{current_month_revenue:,}".replace(",", ".")
    
    monthly_sales_json = {
        "labels": monthly_sales["labels"],
        "data": monthly_sales["data"]
    }
    
    category_sales_json = {
        "categories": category_sales["categories"],
        "sales": category_sales["sales"]
    }
    
    return render_template("admin/dashboard.html",
                           total_products=total_products,
                           total_orders=total_orders,
                           total_users=total_users,
                           total_revenue=formatted_total_revenue,
                           current_month_revenue=formatted_month_revenue,
                           revenue_growth=f"{revenue_growth:.1f}",
                           new_users=new_users_count,
                           user_growth=f"{user_growth:.1f}",
                           monthly_sales=monthly_sales_json,
                           category_sales=category_sales_json,
                           top_products=top_products)