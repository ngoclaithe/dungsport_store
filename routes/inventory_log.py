from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.inventory_log import InventoryLog
from models.product import Product
from datetime import datetime

inventory_bp = Blueprint("inventory", __name__, url_prefix='/inventory')

@inventory_bp.route("/")
def list_inventory():
    inventory_logs = InventoryLog.query.all()
    return render_template("admin/inventory_log.html", inventory_logs=inventory_logs)

@inventory_bp.route("/add", methods=["GET", "POST"])
def add_inventory():
    if request.method == "POST":
        id_product = request.form["id_product"]
        change_quantity = int(request.form["change_quantity"])
        change_type = request.form["change_type"]
        note = request.form["note"]
        
        product = Product.query.get_or_404(id_product)
        
        if change_type == "import":  
            product.inventory += change_quantity
        elif change_type == "export":  
            if product.inventory >= change_quantity:
                product.inventory -= change_quantity
            else:
                flash("Số lượng xuất hàng vượt quá số lượng tồn kho hiện tại!", "danger")
                products = Product.query.all()
                return render_template("admin/inventory_form.html", products=products)
        
        new_log = InventoryLog(
            id_product=id_product,
            change_quantity=change_quantity,
            change_type=change_type,
            log_date=datetime.now(),
            note=note
        )
        
        db.session.add(new_log)
        db.session.commit()
        
        flash("Bản ghi kiểm kê đã được thêm thành công và số lượng tồn kho đã được cập nhật!", "success")
        return redirect(url_for("inventory.list_inventory"))
    
    products = Product.query.all()
    return render_template("admin/inventory_form.html", products=products)

@inventory_bp.route("/edit/<int:id_log>", methods=["GET"])
def edit_inventory(id_log):
    log = InventoryLog.query.get_or_404(id_log)
    products = Product.query.all()
    return render_template("admin/inventory_form.html", log=log, products=products)

@inventory_bp.route("/update/<int:id_log>", methods=["POST"])
def update_inventory(id_log):
    old_log = InventoryLog.query.get_or_404(id_log)
    old_product_id = old_log.id_product
    old_quantity = int(old_log.change_quantity)
    old_type = old_log.change_type
    
    new_product_id = request.form["id_product"]
    new_quantity = int(request.form["change_quantity"])
    new_type = request.form["change_type"]
    
    old_product = Product.query.get_or_404(old_product_id)
    if old_type == "import":
        old_product.inventory -= old_quantity
    elif old_type == "export":
        old_product.inventory += old_quantity
    
    new_product = Product.query.get_or_404(new_product_id)
    
    if new_type == "export" and new_product.inventory < new_quantity:
        flash("Số lượng xuất hàng vượt quá số lượng tồn kho hiện tại!", "danger")
        products = Product.query.all()
        return render_template("admin/inventory_form.html", log=old_log, products=products)
    
    if new_type == "import":
        new_product.inventory += new_quantity
    elif new_type == "export":
        new_product.inventory -= new_quantity
    
    old_log.id_product = new_product_id
    old_log.change_quantity = new_quantity
    old_log.change_type = new_type
    old_log.note = request.form["note"]
    
    db.session.commit()
    
    flash("Bản ghi kiểm kê đã được cập nhật thành công và số lượng tồn kho đã được điều chỉnh!", "success")
    return redirect(url_for("inventory.list_inventory"))

@inventory_bp.route("/delete/<int:id_log>", methods=["POST"])
def delete_inventory(id_log):
    log = InventoryLog.query.get_or_404(id_log)
    
    product = Product.query.get_or_404(log.id_product)
    
    if log.change_type == "import":
        product.inventory -= int(log.change_quantity)
    elif log.change_type == "export":
        product.inventory += int(log.change_quantity)
    
    db.session.delete(log)
    db.session.commit()
    
    flash("Bản ghi kiểm kê đã được xóa thành công và số lượng tồn kho đã được điều chỉnh!", "success")
    return redirect(url_for("inventory.list_inventory"))