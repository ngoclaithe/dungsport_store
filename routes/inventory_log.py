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
        new_log = InventoryLog(
            id_product=request.form["id_product"],
            change_quantity=request.form["change_quantity"],
            change_type=request.form["change_type"],
            log_date=datetime.now(),
            note=request.form["note"]
        )
        db.session.add(new_log)
        db.session.commit()
        flash("Bản ghi kiểm kê đã được thêm thành công!", "success")
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
    log = InventoryLog.query.get_or_404(id_log)
    log.id_product = request.form["id_product"]
    log.change_quantity = request.form["change_quantity"]
    log.change_type = request.form["change_type"]
    log.note = request.form["note"]
    db.session.commit()
    flash("Bản ghi kiểm kê đã được cập nhật thành công!", "success")
    return redirect(url_for("inventory.list_inventory"))

@inventory_bp.route("/delete/<int:id_log>", methods=["POST"])
def delete_inventory(id_log):
    log = InventoryLog.query.get_or_404(id_log)
    db.session.delete(log)
    db.session.commit()
    flash("Bản ghi kiểm kê đã được xóa thành công!", "success")
    return redirect(url_for("inventory.list_inventory"))