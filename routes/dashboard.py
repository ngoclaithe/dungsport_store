from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db  
from models.product import Product
from models.order import Order
from models.user import User
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

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

@dashboard_bp.route("/dashboard")
@admin_required
def dashboard():
    total_products = db.session.query(Product).count()
    total_orders = db.session.query(Order).count()
    total_users = db.session.query(User).count()

    return render_template("admin/dashboard.html",
                           total_products=total_products,
                           total_orders=total_orders,
                           total_users=total_users)
