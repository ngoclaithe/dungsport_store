
document.addEventListener('DOMContentLoaded', function() {

    updateCartDisplay();
    
    const checkoutBtn = document.getElementById('checkout-btn');
    if (checkoutBtn) {
        checkoutBtn.addEventListener('click', function() {
            window.location.href = '/checkout';  
        });
    }
});

function updateCartDisplay() {
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    const cartGrid = document.querySelector('.liked-products-grid');
    
    if (cart.length === 0) {
        cartGrid.innerHTML = `
            <div class="empty-cart">
                <i class="fas fa-shopping-cart"></i>
                <p>Giỏ hàng của bạn đang trống.</p>
                <a href="/" class="continue-shopping">Tiếp tục mua sắm</a>
            </div>
        `;
        return;
    }

    let cartHTML = '';
    let subtotal = 0;

    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        subtotal += itemTotal;
        
        cartHTML += `
            <div class="cart-item" data-index="${index}">
                <div class="remove-item" onclick="removeItem(${index})">
                    <i class="fas fa-times"></i>
                </div>
                <img src="${item.image}" alt="${item.name}" class="cart-item-image">
                <div class="cart-item-info">
                    <h3 class="cart-item-name">${item.name}</h3>
                    <p class="cart-item-brand">Thương hiệu: ${item.brand || 'Không có'}</p>
                    ${item.size ? `<p class="cart-item-size">Kích thước: ${item.size}</p>` : ''}
                    ${item.color ? `<p class="cart-item-color">Màu sắc: ${item.color}</p>` : ''}
                    <p class="cart-item-price">Giá: ${formatCurrency(item.price)}</p>
                    <div class="cart-item-quantity">
                        Số lượng: 
                        <div class="quantity-controls">
                            <button class="quantity-btn" onclick="updateQuantity(${index}, -1)">-</button>
                            <input type="text" class="quantity-value" value="${item.quantity}" onchange="updateQuantityInput(${index}, this.value)">
                            <button class="quantity-btn" onclick="updateQuantity(${index}, 1)">+</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
    });

    const shippingFee = subtotal > 500000 ? 0 : 30000;
    const total = subtotal + shippingFee;

    cartHTML += `
        <div class="cart-summary">
            <div class="cart-summary-row">
                <span>Tạm tính:</span>
                <span>${formatCurrency(subtotal)}</span>
            </div>
            <div class="cart-summary-row">
                <span>Phí vận chuyển:</span>
                <span>${formatCurrency(shippingFee)}</span>
            </div>
            <div class="cart-summary-row total">
                <span>Tổng cộng:</span>
                <span>${formatCurrency(total)}</span>
            </div>
            <button id="checkout-btn" class="checkout-btn">Tiến hành thanh toán</button>
        </div>
    `;

    cartGrid.innerHTML = cartHTML;
    
    updateCartBadge();
}

function updateQuantity(index, change) {
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    
    if (cart[index]) {
        cart[index].quantity += change;
        
        if (cart[index].quantity < 1) {
            cart[index].quantity = 1;
        }
        
        localStorage.setItem('dungsport_cart', JSON.stringify(cart));
        updateCartDisplay();
    }
}

function updateQuantityInput(index, value) {
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    
    if (cart[index]) {
        const quantity = Math.max(1, parseInt(value) || 1);
        cart[index].quantity = quantity;
        
        localStorage.setItem('dungsport_cart', JSON.stringify(cart));
        updateCartDisplay();
    }
}

function removeItem(index) {
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    
    if (confirm('Bạn có chắc chắn muốn xóa sản phẩm này khỏi giỏ hàng?')) {
        cart.splice(index, 1);
        localStorage.setItem('dungsport_cart', JSON.stringify(cart));
        updateCartDisplay();
    }
}

function updateCartBadge() {
    const cart = JSON.parse(localStorage.getItem('dungsport_cart')) || [];
    const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
    
    const badges = document.querySelectorAll('.fas.fa-shopping-cart + .badge');
    badges.forEach(badge => {
        badge.textContent = totalItems;
    });
}

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', { 
        style: 'currency', 
        currency: 'VND' 
    }).format(amount);
}