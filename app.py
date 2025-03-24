import logging
from flask import Flask, request, json
from waitress import serve
from models import db, init_db
from routes.dashboard import dashboard_bp
from routes.category import category_bp
from routes.order import order_bp
from routes.product import product_bp
from routes.user import user_bp
from routes.brand import brand_bp
from routes.upload import upload_bp
from routes.product_image import product_image_bp
from routes.main import main_bp
from routes.api import api_bp
from routes.payment import payment_bp
from routes.inventory_log import inventory_bp

from config import Config

app = Flask(__name__, static_folder='static', static_url_path='/static')
app.jinja_env.filters['tojson'] = json.dumps
app.config.from_object(Config)

init_db(app)
app.register_blueprint(dashboard_bp)
app.register_blueprint(category_bp)
app.register_blueprint(order_bp)
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)
app.register_blueprint(brand_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(product_image_bp)
app.register_blueprint(main_bp)
app.register_blueprint(api_bp)
app.register_blueprint(payment_bp)
app.register_blueprint(inventory_bp)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),                    
    ]
)

@app.before_request
def log_request_info():
    # logging.info(f"Request: {request.method} {request.path}")
    # logging.info(f"Headers: {request.headers}")
    logging.info(f"Body: {request.get_data()}")

# @app.after_request
# def log_response_info(response):
#     logging.info(f"Response status: {response.status}")
#     return response

if __name__ == "__main__":
    logging.info("Server đang chạy trên 0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000)
