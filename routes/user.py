from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.staff import Staff
from models.user import User
user_bp = Blueprint("user", __name__, url_prefix='/user')

@user_bp.route("/")
def list_user():
    users = User.query.all()
    return render_template("admin/user.html", users=users)

@user_bp.route("/add", methods=["POST"])
def add_user():
    new_user = User(
        fullname=request.form["fullname"],
        email=request.form["email"],
        phone=request.form["phone"]
    )
    db.session.add(new_user)
    db.session.commit()
    flash("Người dùng đã được thêm!")
    return redirect(url_for("user.list_user"))
