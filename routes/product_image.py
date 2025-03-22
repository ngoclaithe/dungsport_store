from flask import Blueprint, request, jsonify
from models import db
from models.product import Product
from models.product_image import ProductImage
product_image_bp = Blueprint("product_image", __name__, url_prefix='/product_image')

@product_image_bp.route("/<int:id_product>/images", methods=["GET"])
def list_product_images(id_product):
    product = Product.query.get_or_404(id_product)
    images = [{"id_image": img.id_image, "image_url": img.image_url} for img in product.images]
    return jsonify({"product_id": id_product, "images": images})

@product_image_bp.route("/<int:id_product>/images/add", methods=["POST"])
def add_product_image(id_product):
    product = Product.query.get_or_404(id_product)
    
    if len(product.images) >= 4:
        return jsonify({"success": False, "message": "Một sản phẩm chỉ có thể có tối đa 4 ảnh"}), 400
    
    image_url = request.form.get("image_url")
    if not image_url:
        return jsonify({"success": False, "message": "Đường dẫn ảnh là bắt buộc"}), 400
    
    new_image = ProductImage(id_product=id_product, image_url=image_url)
    db.session.add(new_image)
    db.session.commit()
    
    return jsonify({"success": True, "message": "Ảnh đã được thêm", "id_image": new_image.id_image})

@product_image_bp.route("/images/<int:id_image>/delete", methods=["DELETE"])
def delete_product_image(id_image):
    image = ProductImage.query.get_or_404(id_image)
    db.session.delete(image)
    db.session.commit()
    return jsonify({"success": True, "message": "Ảnh đã được xóa"})