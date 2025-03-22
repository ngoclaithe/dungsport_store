from flask import Blueprint, render_template, request, redirect, url_for, flash 
from models import db 
from models.order import Order 
from models.order_detail import OrderDetail 
from models.product import Product 
from models.product_image import ProductImage 
from models.payment import Payment 
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

order_bp = Blueprint("order", __name__, url_prefix='/order') 

def send_email(receiver_email, subject, message):
    sender_email = "newli5737@gmail.com"
    password = "cige dcqz upbz nbaq"
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    
    msg.attach(MIMEText(message, 'html'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_email_async(receiver_email, subject, message):
    thread = threading.Thread(target=send_email, args=(receiver_email, subject, message))
    thread.start()

@order_bp.route("/") 
def orders(): 
    orders = Order.query.all() 
    return render_template("admin/order.html", orders=orders) 

@order_bp.route("/update/<string:order_id>", methods=["POST"]) 
def update_order(order_id): 
    order = Order.query.filter_by(order_id=order_id).first()
    if order: 
        new_status = request.form["status"]
        order.status = new_status
        
        if new_status == "approved":
            new_payment = Payment(
                id_order=order.id,
                amount=order.total,
                payment_method=order.payment_method,
                payment_date=datetime.now(),
                status="paid"
            )
            db.session.add(new_payment)
            
            subject = "Xác nhận đơn hàng thành công"
            message = f"""
            <html>
            <body>
                <h2>Xác nhận đơn hàng thành công</h2>
                <p>Xin chào {order.customer_fullname},</p>
                <p>Đơn hàng của bạn (Mã đơn: {order.order_id}) đã được xác nhận và đang được xử lý.</p>
                <p><strong>Thông tin đơn hàng:</strong></p>
                <ul>
                    <li>Tổng giá trị: {order.total:,.0f} VNĐ</li>
                    <li>Phương thức thanh toán: {order.payment_method}</li>
                    <li>Địa chỉ giao hàng: {order.customer_address_detail}, {order.customer_ward}, {order.customer_district}, {order.customer_province}</li>
                </ul>
                <p>Cảm ơn bạn đã mua sắm cùng chúng tôi!</p>
            </body>
            </html>
            """
            send_email_async(order.customer_email, subject, message)
            
        elif new_status == "refused":
            subject = "Thông báo đơn hàng không thành công"
            message = f"""
            <html>
            <body>
                <h2>Thông báo đơn hàng không thành công</h2>
                <p>Xin chào {order.customer_fullname},</p>
                <p>Chúng tôi rất tiếc phải thông báo rằng đơn hàng của bạn (Mã đơn: {order.order_id}) không thể được xử lý.</p>
                <p>Vui lòng liên hệ với chúng tôi để biết thêm thông tin chi tiết.</p>
                <p>Chúng tôi xin lỗi vì sự bất tiện này và hy vọng sẽ được phục vụ bạn trong tương lai.</p>
            </body>
            </html>
            """
            send_email_async(order.customer_email, subject, message)
        
        db.session.commit() 
        flash("Cập nhật đơn hàng thành công!") 
    else:
        flash("Không tìm thấy đơn hàng!")
    return redirect(url_for("order.orders")) 

@order_bp.route("/detail/<string:order_id>") 
def order_detail(order_id): 
    order = Order.query.filter_by(order_id=order_id).first() 
    if not order: 
        flash("Đơn hàng không tồn tại!") 
        return redirect(url_for("order.orders")) 
     
    order_details = OrderDetail.query.filter_by(order_id=order.id).all() 
    return render_template("admin/order_detail.html", order=order, order_details=order_details)
