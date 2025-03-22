from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.brand import Brand

brand_bp = Blueprint("brand", __name__, url_prefix='/brand')

@brand_bp.route("/")
def list_brands():
    brands = Brand.query.all()
    return render_template("admin/brand.html", brands=brands)

@brand_bp.route("/add", methods=["GET", "POST"])
def add_brand():
    if request.method == "POST":
        brand_name = request.form.get("brand_name")
        description = request.form.get("description")
        if brand_name:
            new_brand = Brand(brand_name=brand_name, description=description)
            db.session.add(new_brand)
            db.session.commit()
            flash("Thương hiệu đã được thêm!", "success")
            return redirect(url_for("brand.list_brands"))
        else:
            flash("Thiếu tên thương hiệu", "error")
    return render_template("admin/brand_form.html")  

@brand_bp.route("/edit/<int:id_brand>", methods=["GET", "POST"])
def edit_brand(id_brand):
    brand = Brand.query.get_or_404(id_brand)
    if request.method == "POST":
        brand.brand_name = request.form.get("brand_name")
        brand.description = request.form.get("description")
        db.session.commit()
        flash("Thương hiệu đã được cập nhật!", "success")
        return redirect(url_for("brand.list_brands"))
    return render_template("admin/brand_form.html", brand=brand)

@brand_bp.route("/delete/<int:id_brand>", methods=["POST"])
def delete_brand(id_brand):
    brand = Brand.query.get_or_404(id_brand)
    db.session.delete(brand)
    db.session.commit()
    flash("Thương hiệu đã được xóa!", "success")
    return redirect(url_for("brand.list_brands"))
