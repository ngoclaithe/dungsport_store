from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.product import Product
from models.category import Category
from models.brand import Brand
from models.product_image import ProductImage
from datetime import datetime

product_bp = Blueprint("product", __name__, url_prefix='/product')

@product_bp.route("/")
def list_products():
    products = Product.query.all()
    return render_template("admin/product.html", products=products)

@product_bp.route("/add", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        product_name = request.form.get("product_name")
        id_category = request.form.get("id_category")
        id_brand = request.form.get("id_brand")
        price = request.form.get("price")
        cost_price = request.form.get("cost_price")
        inventory = request.form.get("inventory")
        description = request.form.get("description")
        size = request.form.get("size")
        color = request.form.get("color")        
        discount = request.form.get("discount")    
        # image_url = request.form.get("image_url")
        
        if product_name and price:
            new_product = Product(
                product_name=product_name,
                id_category=int(id_category) if id_category else 0,
                id_brand=int(id_brand) if id_brand else 0,
                price=float(price),
                cost_price=float(cost_price) if cost_price else 0.0,
                inventory=int(inventory) if inventory else 0,
                description=description,
                size=size,
                color=color,
                created_at=datetime.now(),
                discount=discount
                # image_url=image_url
            )
            db.session.add(new_product)
            db.session.commit()
            flash("Sản phẩm đã được thêm!", "success")
            return redirect(url_for("product.list_products"))
        else:
            flash("Thiếu thông tin bắt buộc", "error")
    
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template("admin/product_form.html", categories=categories, brands=brands)

@product_bp.route("/edit/<int:id_product>", methods=["GET", "POST"])
def edit_product(id_product):
    product = Product.query.get_or_404(id_product)
    if request.method == "POST":
        product.product_name = request.form.get("product_name")
        product.id_category = int(request.form.get("id_category"))
        product.id_brand = int(request.form.get("id_brand"))
        product.price = float(request.form.get("price"))
        cost_price = request.form.get("cost_price")
        product.cost_price = float(cost_price) if cost_price else 0.0
        inventory = request.form.get("inventory")
        product.inventory = int(inventory) if inventory else 0
        product.description = request.form.get("description")
        product.size = request.form.get("size")
        product.color = request.form.get("color")  
        product.discount = request.form.get("discount")    
        # product.image_url = request.form.get("image_url")
        
        db.session.commit()
        flash("Sản phẩm đã được cập nhật!", "success")
        return redirect(url_for("product.list_products"))
    
    categories = Category.query.all()
    brands = Brand.query.all()
    return render_template("admin/product_form.html", product=product, categories=categories, brands=brands)

@product_bp.route("/delete/<int:id_product>", methods=["POST"])
def delete_product(id_product):
    product = Product.query.get_or_404(id_product)
    db.session.delete(product)
    db.session.commit()
    flash("Sản phẩm đã được xóa!", "success")
    return redirect(url_for("product.list_products"))

@product_bp.route("/detail/<int:id_product>", methods=["GET"])
def add_detail_product_form(id_product):
    product = Product.query.get_or_404(id_product)
    return render_template("admin/add_detail_product_form.html", product=product)

