document.addEventListener('DOMContentLoaded', function() {
    const navContainer = document.querySelector('.navigation');
    navContainer.style.position = 'relative';
    const navMenu = document.querySelector('.nav-menu');
    const categoryItem = navMenu.querySelector('.nav-item');
    let categoryContainer = document.querySelector('.category-container');
    if (!categoryContainer) {
        categoryContainer = document.createElement('div');
        categoryContainer.classList.add('category-container');
        Object.assign(categoryContainer.style, {
            display: 'none',
            position: 'absolute',
            backgroundColor: '#fff',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            padding: '10px',
            zIndex: '9999',
            borderRadius: '4px',
            width: '800px',
            maxHeight: '400px',
            overflowY: 'auto',
            gridTemplateColumns: 'repeat(5, 1fr)',
            gap: '10px'
        });
        navContainer.appendChild(categoryContainer);
    }
    categoryItem.addEventListener('click', function(e) {
        e.stopPropagation();
        if (categoryContainer.style.display === 'none' || categoryContainer.style.display === '') {
            categoryContainer.style.top = categoryItem.offsetHeight + 'px';
            categoryContainer.style.left = '0px';
            categoryContainer.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 8px;"><i class="fas fa-spinner fa-spin"></i></div>`;
            categoryContainer.style.display = 'grid';
            fetch('/api/list_category')
                .then(response => response.json())
                .then(data => {
                    if (!data || data.length === 0) {
                        categoryContainer.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 8px; color: red;">Không có danh mục nào.</div>`;
                        return;
                    }
                    categoryContainer.innerHTML = '';
                    data.forEach(category => {
                        const catDiv = document.createElement('div');
                        catDiv.classList.add('category-item');
                        catDiv.dataset.id = category.id_category;
                        catDiv.textContent = category.category_name;
                        Object.assign(catDiv.style, {
                            padding: '8px',
                            cursor: 'pointer',
                            textAlign: 'center',
                            borderRadius: '4px',
                            backgroundColor: '#f9f9f9',
                            transition: 'background-color 0.3s'
                        });
                        catDiv.addEventListener('mouseenter', function() {
                            catDiv.style.backgroundColor = '#e0e0e0';
                        });
                        catDiv.addEventListener('mouseleave', function() {
                            catDiv.style.backgroundColor = '#f9f9f9';
                        });
                        catDiv.addEventListener('click', function() {
                            window.location.href = `/list-category/${encodeURIComponent(category.id_category)}`;
                        });
                        categoryContainer.appendChild(catDiv);
                    });
                })
                .catch(error => {
                    console.error('Error fetching categories:', error);
                    categoryContainer.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 8px; color: red;"><i class="fas fa-exclamation-circle"></i> Lỗi tải danh mục.</div>`;
                });
        } else {
            categoryContainer.style.display = 'none';
        }
    });
    document.addEventListener('click', function(e) {
        if (categoryContainer && !categoryContainer.contains(e.target) && !categoryItem.contains(e.target)) {
            categoryContainer.style.display = 'none';
        }
    });
});
