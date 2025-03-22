from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db

main_bp = Blueprint("main", __name__, url_prefix='/')

@main_bp.route("/")
def home():
    return render_template("index.html")

@main_bp.route("/address_store")
def address_store():
    return render_template("address.html")

@main_bp.route("/my-order-cart")
def my_order_cart():
    return render_template("order-cart.html")

@main_bp.route("/create-order")
def create_order():
    return render_template("order.html")

@main_bp.route("/like-product")
def like_product():
    return render_template("like_product.html")

@main_bp.route("/checkout")
def check_out():
    return render_template("checkout.html")

@main_bp.route("/login")
def login():
    return render_template("login.html")

@main_bp.route("/profile")
def profile_user():
    return render_template("profile_user.html")

@main_bp.route("/detail-product/<int:product_id>")
def detail_product(product_id):
    return render_template("detail_product.html")

@main_bp.route("/list-category/<int:id_category>")
def list_category(id_category):
    return render_template("list_category.html")