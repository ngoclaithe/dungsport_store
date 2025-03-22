from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.category import Category
from datetime import datetime

category_bp = Blueprint("category", __name__, url_prefix='/category')

@category_bp.route("/")
def categories():
    categories = Category.query.all()
    return render_template("admin/category.html", categories=categories)

@category_bp.route("/add", methods=["POST"])
def add_category():
    new_category = Category(
        category_name=request.form["name"],
        description=request.form["description"],
        created_at=datetime.now()
    )
    db.session.add(new_category)
    db.session.commit()
    flash("Danh mục đã được thêm thành công!")
    return redirect(url_for("category.categories"))

@category_bp.route("/edit/<int:category_id>", methods=["GET"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    categories = Category.query.all()
    return render_template("admin/category.html", categories=categories, edit_category=category)

@category_bp.route("/update/<int:category_id>", methods=["POST"])
def update_category(category_id):
    category = Category.query.get_or_404(category_id)
    category.category_name = request.form["name"]
    category.description = request.form["description"]
    db.session.commit()
    flash("Danh mục đã được cập nhật thành công!")
    return redirect(url_for("category.categories"))

@category_bp.route("/delete/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("Danh mục đã được xóa thành công!")
    return redirect(url_for("category.categories"))