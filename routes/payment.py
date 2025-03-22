from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.payment import Payment

payment_bp = Blueprint("payment", __name__, url_prefix='/payment')

@payment_bp.route("/")
def list_payments():
    payments = Payment.query.all()
    return render_template("admin/payment.html", payments=payments)