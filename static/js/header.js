document.querySelector('.header .logo').addEventListener('click', function () {
    window.location.href = '/';
});

document.querySelector('.user-actions .fa-globe').addEventListener('click', function () {
    window.location.href = '/address_store';
});

document.querySelector('.fa-heart').addEventListener('click', function () {
    window.location.href = '/like-product';
});

document.querySelector('.fa-shopping-cart').addEventListener('click', function () {
    window.location.href = '/my-order-cart';
});

const searchInput = document.querySelector('.search-bar input');
const searchResultsContainer = document.createElement('div');
searchResultsContainer.className = 'search-results';
searchResultsContainer.style.display = 'none';
searchResultsContainer.style.position = 'absolute';
searchResultsContainer.style.width = '100%';
searchResultsContainer.style.maxHeight = '400px';
searchResultsContainer.style.overflowY = 'auto';
searchResultsContainer.style.backgroundColor = '#fff';
searchResultsContainer.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
searchResultsContainer.style.zIndex = '1000';
searchResultsContainer.style.borderRadius = '0 0 4px 4px';

const searchBar = document.querySelector('.search-bar');
searchBar.style.position = 'relative';
searchBar.appendChild(searchResultsContainer);

function searchProducts(query) {
    if (!query || query.trim() === '') {
        searchResultsContainer.style.display = 'none';
        return;
    }

    fetch(`/api/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            searchResultsContainer.innerHTML = '';
            
            if (data.length === 0) {
                searchResultsContainer.innerHTML = '<div class="no-results" style="padding: 10px; text-align: center;">Không tìm thấy sản phẩm nào</div>';
                searchResultsContainer.style.display = 'block';
                return;
            }
            
            data.forEach(product => {
                const productElement = document.createElement('div');
                productElement.className = 'search-item';
                productElement.style.padding = '10px';
                productElement.style.borderBottom = '1px solid #eee';
                productElement.style.display = 'flex';
                productElement.style.alignItems = 'center';
                productElement.style.cursor = 'pointer';
                
                const imageUrl = product.image_url || '/static/images/no-image.jpg';
                
                productElement.innerHTML = `
                    <img src="${imageUrl}" alt="${product.product_name}" style="width: 50px; height: 50px; object-fit: cover; margin-right: 10px;">
                    <div>
                        <div style="font-weight: bold;">${product.product_name}</div>
                        <div>${new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.price)}</div>
                    </div>
                `;
                
                productElement.addEventListener('click', () => {
                    window.location.href = `/detail-product/${product.id}`;
                });
                
                searchResultsContainer.appendChild(productElement);
            });
            
            searchResultsContainer.style.display = 'block';
        })
        .catch(error => {
            console.error('Lỗi khi tìm kiếm sản phẩm:', error);
            searchResultsContainer.innerHTML = '<div class="no-results" style="padding: 10px; text-align: center;">Đã xảy ra lỗi khi tìm kiếm</div>';
            searchResultsContainer.style.display = 'block';
        });
}

function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

const debouncedSearch = debounce(searchProducts, 300);

if (searchInput) {
    searchInput.addEventListener('input', function() {
        debouncedSearch(this.value);
    });

    searchInput.addEventListener('keypress', function(event) {
        if (event.key === 'Enter') {
            const query = this.value.trim();
            if (query !== '') {
                window.location.href = `/search?q=${encodeURIComponent(query)}`;
            }
        }
    });
}

document.addEventListener('click', function(event) {
    if (searchInput && !searchInput.contains(event.target) && !searchResultsContainer.contains(event.target)) {
        searchResultsContainer.style.display = 'none';
    }
});

document.querySelector('.search-bar button').addEventListener('click', function () {
    if (searchInput) {
        const query = searchInput.value.trim();
        if (query !== '') {
            window.location.href = `/search?q=${encodeURIComponent(query)}`;
        }
    }
});

document.querySelector('.fa-user').addEventListener('click', function () {
    const token = localStorage.getItem("token");
    console.log("Giá trị hiện tại token:", token);
    if(token && token.trim() !== "") {
        window.location.href = '/profile';
    } else {
        window.location.href = '/login';
    }
});

function loadFavorites() {
    const favorites = JSON.parse(localStorage.getItem('favorites')) || [];
    const badge = document.querySelector('.action-item .badge');
    if (badge) {
        badge.textContent = favorites.length;
    }
}

function updateCartCount() {
    const cart = JSON.parse(localStorage.getItem('cart')) || [];
    const cartBadge = document.querySelector('.fa-shopping-cart').nextElementSibling;
    if (cartBadge) {
        cartBadge.textContent = cart.reduce((total, item) => total + (item.quantity || 1), 0);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    loadFavorites();
    updateCartCount();
});