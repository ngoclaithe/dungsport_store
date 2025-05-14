from flask import Blueprint, request, jsonify
from models import db
from models.brand import Brand
from models.product import Product
from models.category import Category
from models.product_image import ProductImage
from models.order import Order
from models.order_detail import OrderDetail
from datetime import datetime, timedelta
from fuzzywuzzy import fuzz
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from models.user import User
from config import Config

api_bp = Blueprint("api", __name__, url_prefix='/api')
@api_bp.route("/product_catalog")
def list_category_and_products():
    target_categories = ["cầu lông", "pickleball", "bóng rổ", "bóng chuyền"]
    
    image_map = {
        "cầu lông": "/static/images/danhmuc_caulong.jpg",
        "pickleball": "/static/images/danhmuc_pickleball.jpg",
        "bóng rổ": "/static/images/danhmuc_bongro.jpg",
        "bóng chuyền": "/static/images/danhmuc_bongchuyen.jpg"
    }
    
    data = []
    for target in target_categories:
        categories = Category.query.filter(
            Category.category_name.ilike(f"%{target}%")
        ).all()
        
        total_count = 0
        for cat in categories:
            product_count = len(cat.products) if hasattr(cat, "products") else \
                Product.query.filter_by(id_category=cat.id_category).count()
            total_count += product_count
        
        data.append({
            "name": target,
            "count": total_count,
            "image": image_map.get(target)
        })
    
    return jsonify(data)

@api_bp.route("/list_category", methods=["GET"])
def list_category():
    categories = Category.query.with_entities(Category.id_category, Category.category_name).all()
    
    category_list = [{"id_category": cat[0], "category_name": cat[1]} for cat in categories]
    sorted_categories = sort_categories_by_similarity(category_list)
    return jsonify(sorted_categories)

def sort_categories_by_similarity(categories):
    """
    Sắp xếp danh sách category dựa trên độ tương đồng giữa các tên.
    """
    if not categories:
        return []
    
    sorted_list = [categories[0]]  
    
    for category in categories[1:]:
        best_index = 0
        best_score = 0
        
        for i in range(len(sorted_list)):
            score = fuzz.ratio(category["category_name"], sorted_list[i]["category_name"])
            if score > best_score:
                best_score = score
                best_index = i
        
        sorted_list.insert(best_index + 1, category)
    
    return sorted_list
@api_bp.route("/get_category/<sport_type>", methods=["GET"])
def get_category(sport_type):
    """
    Tìm kiếm các danh mục liên quan đến một loại thể thao cụ thể dựa trên từ khóa đơn giản.
    
    Args:
        sport_type (str): Từ khóa đơn giản như 'bongro', 'pickeball', 'bongchuyen', 'caulong'
    
    Returns:
        JSON: Danh sách các danh mục thỏa mãn điều kiện tìm kiếm
    """
    sport_mapping = {
        "bongro": "bóng rổ",
        "bongchuyen": "bóng chuyền",
        "pickeball": "pickleball",
        "caulong": "cầu lông"
    }
    
    search_keyword = sport_mapping.get(sport_type.lower(), sport_type)
    
    categories = Category.query.filter(
        Category.category_name.ilike(f"%{search_keyword}%")
    ).all()
    
    result = []
    for category in categories:
        product_count = len(category.products) if hasattr(category, "products") else \
            Product.query.filter_by(id_category=category.id_category).count()
            
        result.append({
            "id_category": category.id_category,
            "category_name": category.category_name,
            "product_count": product_count
        })
    
    return jsonify(result)
@api_bp.route("/product_by_category/<int:id_category>", methods=["GET"])
def list_product_by_id_category(id_category):
    products = Product.query.filter_by(id_category=id_category).all()
    product_list = []
    
    for product in products:
        images = [img.image_url for img in product.images] if product.images else []
        product_list.append({
            "id": product.id_product,
            "product_name": product.product_name,
            "price": float(product.price),
            "images": images
        })
    
    return jsonify(product_list)
@api_bp.route("/product_on_sale_best")
def get_list_8_products_best_sale():
    sale_products = Product.query.filter(Product.discount > 0)\
                        .order_by(Product.discount.desc()).limit(8).all()
    
    data = []
    for product in sale_products:
        image_url = product.images[0].image_url if product.images and len(product.images) > 0 else None
        data.append({
            "id": product.id_product,
            "product_name": product.product_name,
            "price": float(product.price),
            "discount": float(product.discount),
            "image_url": image_url
        })
    return jsonify(data)


@api_bp.route("/new_arrival")
def get_list_new_arrival():
    products = Product.query.order_by(Product.created_at.desc()).limit(10).all()
    
    data = []
    for product in products:
        image_url = product.images[0].image_url if product.images and len(product.images) > 0 else None
        product_data = {
            "id": product.id_product,
            "product_name": product.product_name,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "price": float(product.price),
            "image_url": image_url
        }
        data.append(product_data)
    
    return jsonify(data)


@api_bp.route("/featured_products")
def get_list_featured_products():
    return jsonify([])
@api_bp.route("/create_order", methods=["POST"])
def create_new_order():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid JSON data"}), 400

    customer = data.get("customer", {})
    address = customer.get("address", {})
    payment = data.get("payment", {})

    order_date_str = data.get("orderDate")
    try:
        order_date = datetime.fromisoformat(order_date_str.replace("Z", "+00:00")) if order_date_str else datetime.utcnow()
    except Exception:
        order_date = datetime.utcnow()

    order_id = "DS" + str(int(datetime.utcnow().timestamp()))[-6:]

    new_order = Order(
        order_id=order_id,
        customer_fullname=customer.get("fullname"),
        customer_email=customer.get("email"),
        customer_phone=customer.get("phone"),
        customer_province=address.get("province"),
        customer_district=address.get("district"),
        customer_ward=address.get("ward"),
        customer_address_detail=address.get("addressDetail"),
        payment_method=payment.get("method"),
        note=data.get("note"),
        subtotal=data.get("subtotal", 0),
        shipping_fee=data.get("shippingFee", 0),
        total=data.get("total", 0),
        order_date=order_date
    )

    db.session.add(new_order)
    db.session.commit()

    items = data.get("items", [])
    for item in items:
        order_detail = OrderDetail(
            order_id=new_order.id,
            id_product=item.get("id"),
            name=item.get("name"),
            image=item.get("image"),
            price=item.get("price"),
            original_price=item.get("originalPrice"),
            quantity=item.get("quantity"),
            color=item.get("color").strip() if item.get("color") else None,
            size=item.get("size").strip() if item.get("size") else None,
            brand=item.get("brand")
        )
        db.session.add(order_detail)

    db.session.commit()

    return jsonify({"message": "Order created successfully", "order_id": order_id}), 201

@api_bp.route("/address_store")
def get_list_address_store():
    addresses = [
        {
            "address": "208i P. Lê Trọng Tấn, Định Công, Thanh Xuân, Hà Nội, Vietnam",
            "latitude": 20.993437894527855,
            "longitude": 105.83167553995564
        },
        {
            "address": "408 Đ. Khương Đình, Hạ Đình, Thanh Xuân, Hà Nội 120120, Vietnam",
            "latitude": 20.988029496609197,
            "longitude": 105.81292589976452
        }
    ]
    return jsonify(addresses)

@api_bp.route("/login", methods=["POST"])
def login():
    data = request.form or request.get_json()
    email = data.get("email")
    password = data.get("password")
    if not email or not password:
        return jsonify({"success": False, "message": "Email và mật khẩu là bắt buộc"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"success": False, "message": "Email hoặc mật khẩu không đúng"}), 401

    token = jwt.encode(
        {"user_id": user.id_user, "exp": datetime.utcnow() + timedelta(hours=1)},
        Config.SECRET_KEY,
        algorithm="HS256"
    )
    return jsonify({"success": True, "token": "Bearer " + token})

@api_bp.route("/search", methods=["GET"])
def search_products():
    query = request.args.get('q', '')
    if not query or len(query.strip()) < 2:
        return jsonify([])
    
    products = Product.query.filter(
        db.or_(
            Product.product_name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%")
        )
    ).limit(10).all()
    
    result = []
    for product in products:
        image_url = product.images[0].image_url if product.images and len(product.images) > 0 else None
        
        category_name = product.category.category_name if product.category else None
        brand_name = product.brand.brand_name if product.brand else None
        
        result.append({
            "id": product.id_product,
            "product_name": product.product_name,
            "price": float(product.price),
            "discount": float(product.discount) if product.discount else 0,
            "category": category_name,
            "brand": brand_name,
            "image_url": image_url
        })
    
    return jsonify(result)

@api_bp.route("/search_page", methods=["GET"])
def search_page_results():
    query = request.args.get('q', '')
    if not query or len(query.strip()) < 2:
        return jsonify({"products": [], "query": query})
    
    products = Product.query.filter(
        db.or_(
            Product.product_name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%")
        )
    ).all()
    
    result = []
    for product in products:
        images = [img.image_url for img in product.images] if product.images else []
        
        category_name = product.category.category_name if product.category else None
        category_id = product.category.id_category if product.category else None
        brand_name = product.brand.brand_name if product.brand else None
        
        result.append({
            "id": product.id_product,
            "product_name": product.product_name,
            "price": float(product.price),
            "discount": float(product.discount) if product.discount else 0,
            "description": product.description,
            "category": category_name,
            "category_id": category_id,
            "brand": brand_name,
            "images": images,
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "size": product.size,
            "color": product.color
        })
    
    return jsonify({
        "products": result,
        "query": query,
        "total": len(result)
    })

@api_bp.route("/info/<int:id_user>", methods=["GET"])
def get_info(id_user):
    user = User.query.get(id_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_info = {
        "id_user": user.id_user,
        "fullname": user.fullname,
        "email": user.email,
        "phone": user.phone,
        "province": user.province,
        "district": user.district,
        "ward": user.ward,
        "address": user.address,
        "role": user.role
    }
    return jsonify(user_info)
@api_bp.route("/info/<int:id_user>", methods=["PUT"])
def update_info(id_user):
    user = User.query.get(id_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()

    if 'fullname' in data:
        user.fullname = data['fullname']
    if 'email' in data:
        user.email = data['email']
    if 'phone' in data:
        user.phone = data['phone']
    if 'province' in data:
        user.province = data['province']
    if 'district' in data:
        user.district = data['district']
    if 'ward' in data:
        user.ward = data['ward']
    if 'address' in data:
        user.address = data['address']

    db.session.commit()

    updated_user_info = {
        "id_user": user.id_user,
        "fullname": user.fullname,
        "email": user.email,
        "phone": user.phone,
        "province": user.province,
        "district": user.district,
        "ward": user.ward,
        "address": user.address
    }
    return jsonify(updated_user_info), 200
@api_bp.route("/register", methods=["POST"])
def register():
    data = request.form or request.get_json()
    fullname = data.get("fullname")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")
    confirm_password = data.get("confirm_password")
    province = data.get("province")
    district = data.get("district")
    ward = data.get("ward")
    address = data.get("address")

    if not (fullname and email and phone and password and confirm_password and province and district and ward and address):
        return jsonify({"success": False, "message": "Vui lòng điền đầy đủ thông tin"}), 400

    if password != confirm_password:
        return jsonify({"success": False, "message": "Mật khẩu không khớp"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"success": False, "message": "Email đã được đăng ký"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        fullname=fullname,
        email=email,
        password_hash=hashed_password,
        phone=phone,
        province=province,
        district=district,
        ward=ward,
        address=address,
        role='customer'
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "Đăng ký thành công"})

@api_bp.route("/product/<int:product_id>")
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({"error": "Product not found"}), 404

    image_urls = [img.image_url for img in product.images] if product.images else []

    product_data = {
        "id": product.id_product,
        "product_name": product.product_name,
        "price": float(product.price),
        "discount": float(product.discount),
        "description": product.description,
        "brand": product.brand.brand_name if product.brand else None,
        "category": product.category.category_name if product.category else None,
        "images": image_urls,
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "size": product.size,
        "color": product.color
    }

    return jsonify(product_data)

