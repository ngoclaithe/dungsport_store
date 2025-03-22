document.addEventListener('DOMContentLoaded', function() {
    checkLoginStatus();
    loadCartProducts();
    setupEventListeners();
    setupLocationOptions();
    updateShippingFee();
});

function checkLoginStatus() {
    const token = localStorage.getItem('token');
    const loginStatusDiv = document.getElementById('login-status');
    
    if (token) {
        try {
            const tokenData = parseJwt(token);
            const userId = tokenData.user_id;
            
            fetch(`/api/info/${userId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Không thể lấy thông tin người dùng');
                }
                return response.json();
            })
            .then(userData => {
                loginStatusDiv.classList.add('logged-in');
                loginStatusDiv.innerHTML = `
                    <p><i class="fas fa-check-circle"></i> Xin chào, <strong>${userData.fullname || 'Khách hàng'}</strong>!</p>
                `;
                
                if (userData.fullname) document.getElementById('fullname').value = userData.fullname;
                if (userData.email) document.getElementById('email').value = userData.email;
                if (userData.phone) document.getElementById('phone').value = userData.phone;
                if (userData.address) document.getElementById('address').value = userData.address;
                
                if (userData.province) {
                    const provinceSelect = document.getElementById('province');
                    provinceSelect.value = userData.province;
                    provinceSelect.dispatchEvent(new Event('change'));
                    if (userData.district) {
                        document.getElementById('district').value = userData.district;
                    }
                    if (userData.ward) {
                        document.getElementById('ward').value = userData.ward;
                    }
                }
            })
            .catch(error => {
                console.error('Lỗi khi lấy thông tin người dùng:', error);
                showLoginOptions();
            });
        } catch (error) {
            console.error('Lỗi khi xử lý token:', error);
            showLoginOptions();
        }
    } else {
        showLoginOptions();
    }
}

function parseJwt(token) {
    try {
      const base64Payload = token.split('.')[1];
      const decodedPayload = atob(base64Payload);
      return JSON.parse(decodedPayload);
    } catch (e) {
      console.error('Token không hợp lệ', e);
      return null;
    }
  }

function showLoginOptions() {
    const loginStatusDiv = document.getElementById('login-status');
    loginStatusDiv.classList.add('not-logged-in');
    loginStatusDiv.innerHTML = `
        <p><i class="fas fa-info-circle"></i> Vui lòng điền đầy đủ thông tin bên dưới để tiến hành đặt hàng</p>
        <div class="login-actions">
            <button class="login-btn" id="login-btn">Đăng nhập</button>
            <button class="register-btn" id="register-btn">Đăng ký</button>
        </div>
    `;
    
    document.getElementById('login-btn').addEventListener('click', function() {
        window.location.href = '/login?redirect=checkout';
    });
    
    document.getElementById('register-btn').addEventListener('click', function() {
        window.location.href = '/register?redirect=checkout';
    });
}

function loadCartProducts() {
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    const cartProductsDiv = document.getElementById('cart-products');
    
    if (cart.length === 0) {
        cartProductsDiv.innerHTML = '<p class="empty-cart-message">Giỏ hàng của bạn đang trống.</p>';
        document.getElementById('place-order-btn').disabled = true;
        return;
    }
    
    let cartHTML = '';
    let subtotal = 0;
    
    cart.forEach((item) => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        cartHTML += `
            <div class="cart-product">
                <img src="${item.image}" alt="${item.name}" class="cart-product-image">
                <div class="cart-product-info">
                    <h4 class="cart-product-name">${item.name}</h4>
                    ${item.size ? `<p class="cart-product-variant">Kích thước: ${item.size}</p>` : ''}
                    ${item.color ? `<p class="cart-product-variant">Màu sắc: ${item.color}</p>` : ''}
                    <div class="cart-product-price-qty">
                        <span class="cart-product-price">${formatCurrency(item.price)}</span>
                        <span class="cart-product-quantity">x ${item.quantity}</span>
                    </div>
                </div>
            </div>
        `;
    });
    
    cartProductsDiv.innerHTML = cartHTML;
    
    document.getElementById('subtotal').textContent = formatCurrency(subtotal);
    calculateTotal();
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount)
        .replace(/\s₫/, ' ₫');
}

function setupEventListeners() {
    const paymentMethods = document.querySelectorAll('input[name="payment_method"]');
    paymentMethods.forEach(method => {
        method.addEventListener('change', function() {
            if (this.value === 'bank-transfer') {
                document.getElementById('bank-details').style.display = 'block';
            } else {
                document.getElementById('bank-details').style.display = 'none';
            }
        });
    });
    
    document.getElementById('province').addEventListener('change', function() {
        updateShippingFee();
    });
    
    document.getElementById('place-order-btn').addEventListener('click', placeOrder);
}

function updateShippingFee() {
    const province = document.getElementById('province').value;
    let shippingFee = 30000; 
    if (province === 'Hà Nội' || province === 'Hồ Chí Minh') {
        shippingFee = 20000;
    } else if (province === 'Đà Nẵng' || province === 'Hải Phòng' || province === 'Cần Thơ') {
        shippingFee = 25000;
    } else if (province === '') {
        shippingFee = 0; 
    }
    
    document.getElementById('shipping-fee').textContent = formatCurrency(shippingFee);
    calculateTotal();
}

function calculateTotal() {
    const subtotalText = document.getElementById('subtotal').textContent;
    const shippingFeeText = document.getElementById('shipping-fee').textContent;
    
    const subtotal = parseFloat(subtotalText.replace(/[^\d]/g, ''));
    const shippingFee = parseFloat(shippingFeeText.replace(/[^\d]/g, ''));
    
    const total = subtotal + shippingFee;
    document.getElementById('total-price').textContent = formatCurrency(total);
}

function setupLocationOptions() {
    const provinces = [
        'Hà Nội', 'Hồ Chí Minh', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
        'An Giang', 'Bà Rịa - Vũng Tàu', 'Bắc Giang', 'Bắc Kạn',
        'Bạc Liêu', 'Bắc Ninh', 'Bến Tre', 'Bình Định', 'Bình Dương'
    ];
    
    const provinceSelect = document.getElementById('province');
    provinceSelect.innerHTML = '<option value="">Chọn Tỉnh/Thành phố</option>';
    
    provinces.forEach(province => {
        const option = document.createElement('option');
        option.value = province;
        option.textContent = province;
        provinceSelect.appendChild(option);
    });
}

function validateForm() {
    const form = document.getElementById('checkout-form');
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');
        } else {
            field.classList.remove('error');
        }
    });
    
    const phoneField = document.getElementById('phone');
    if (phoneField.value && !phoneField.value.match(/^[0-9]{10}$/)) {
        isValid = false;
        phoneField.classList.add('error');
    }
    
    return isValid;
}

function showToast(message, type) {
    let toastContainer = document.getElementById('toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.id = 'toast-container';
        toastContainer.style.position = 'fixed';
        toastContainer.style.top = '20px';
        toastContainer.style.right = '20px';
        toastContainer.style.zIndex = '9999';
        document.body.appendChild(toastContainer);
    }
    const toast = document.createElement('div');
    toast.textContent = message;
    toast.style.background = type === 'success' ? '#4CAF50' : '#f44336';
    toast.style.color = '#fff';
    toast.style.padding = '10px 20px';
    toast.style.marginTop = '10px';
    toast.style.borderRadius = '4px';
    toast.style.boxShadow = '0 2px 6px rgba(0,0,0,0.3)';
    toastContainer.appendChild(toast);
    setTimeout(() => {
        toastContainer.removeChild(toast);
    }, 3000);
}

function placeOrder() {
    if (!validateForm()) {
        showToast('Vui lòng điền đầy đủ thông tin.', 'error');
        return;
    }
    
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    
    if (cart.length === 0) {
        showToast('Giỏ hàng của bạn đang trống.', 'error');
        return;
    }
    
    const orderData = {
        customer: {
            fullname: document.getElementById('fullname').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            address: {
                province: document.getElementById('province').value,
                district: document.getElementById('district').value, 
                ward: document.getElementById('ward').value,          
                addressDetail: document.getElementById('address').value
            }
        },
        items: cart,
        payment: {
            method: document.querySelector('input[name="payment_method"]:checked').value
        },
        note: document.getElementById('order-note').value,
        subtotal: parseFloat(document.getElementById('subtotal').textContent.replace(/[^\d]/g, '')),
        shippingFee: parseFloat(document.getElementById('shipping-fee').textContent.replace(/[^\d]/g, '')),
        total: parseFloat(document.getElementById('total-price').textContent.replace(/[^\d]/g, '')),
        orderDate: new Date().toISOString()
    };
    
    console.log('Order data:', orderData);
    
    fetch('/api/create_order', {
        method: 'POST',
        body: JSON.stringify(orderData)
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Lỗi khi tạo đơn hàng');
        }
        return response.json();
    })
    .then(data => {
        localStorage.setItem('dungsport_cart', JSON.stringify([]));
        showToast('Đặt hàng thành công! Vui lòng kiểm tra email để nhận thông báo.', 'success');
        setTimeout(() => {
            window.location.href = '/';
        }, 3000);
    })
    .catch(error => {
        console.error(error);
        showToast('Đặt hàng thất bại. Vui lòng thử lại sau.', 'error');
    });
}