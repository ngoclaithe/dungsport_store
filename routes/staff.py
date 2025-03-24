from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.staff import Staff
from models.user import User
staff_bp = Blueprint("staff", __name__, url_prefix='/staff')

@staff_bp.route("/")
def list_staff():
    staffs = Staff.query.all()
    users = User.query.filter_by(role='staff').all()
    return render_template("admin/staff.html", staffs=staffs, users=users)

@staff_bp.route("/add", methods=["POST"])
def add_staff():
    new_staff = Staff(
        fullname=request.form["fullname"],
        email=request.form["email"],
        phone=request.form["phone"],
        position=request.form["position"],
        salary=request.form["salary"],
        hire_date=request.form["hire_date"]
    )
    db.session.add(new_staff)
    db.session.commit()
    flash("Thông tin nhân viên đã được thêm!")
    return redirect(url_for("staff.list_staff"))