import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

upload_bp = Blueprint("upload", __name__, url_prefix='/upload')

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload-image", methods=["POST"])
def upload_image():
    if 'product_image' not in request.files:
        return jsonify({'success': False, 'message': 'Không có file nào được gửi'})
    
    file = request.files['product_image']
    
    if file.filename == '':
        return jsonify({'success': False, 'message': 'Không có file nào được chọn'})
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        
        import time
        timestamp = str(int(time.time()))
        filename = timestamp + '_' + filename
        
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        image_url = '/' + filepath.replace('\\', '/')
        
        return jsonify({
            'success': True,
            'image_url': image_url
        })
    
    return jsonify({'success': False, 'message': 'Định dạng file không được hỗ trợ'})