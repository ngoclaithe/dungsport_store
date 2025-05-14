document.addEventListener('DOMContentLoaded', function() {
    const navContainer = document.querySelector('.navigation');
    navContainer.style.position = 'relative';
    const navMenu = document.querySelector('.nav-menu');
    
    const categoryItem = navMenu.querySelector('.nav-item:first-child'); // Danh mục sản phẩm
    const bongRoItem = navMenu.querySelector('.nav-item:nth-child(2)'); // Bóng rổ
    const pickleballItem = navMenu.querySelector('.nav-item:nth-child(3)'); // Pickleball
    const cauLongItem = navMenu.querySelector('.nav-item:nth-child(4)'); // Cầu lông
    const bongChuyenItem = navMenu.querySelector('.nav-item:nth-child(5)'); // Bóng chuyền
    
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
    
    // Tạo container riêng cho các mục thể thao
    let sportCategoryContainer = document.querySelector('.sport-category-container');
    if (!sportCategoryContainer) {
        sportCategoryContainer = document.createElement('div');
        sportCategoryContainer.classList.add('sport-category-container');
        Object.assign(sportCategoryContainer.style, {
            display: 'none',
            position: 'absolute',
            backgroundColor: '#fff',
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            padding: '15px',
            zIndex: '9999',
            borderRadius: '8px',
            width: '600px',
            maxHeight: '450px',
            overflowY: 'auto'
        });
        navContainer.appendChild(sportCategoryContainer);
    }

    categoryItem.addEventListener('click', function(e) {
        e.stopPropagation();
        if (categoryContainer.style.display === 'none' || categoryContainer.style.display === '') {
            showCategoryContainer(categoryItem, 'list_category');
        } else {
            categoryContainer.style.display = 'none';
        }
    });

    bongRoItem.addEventListener('click', function(e) {
        e.stopPropagation();
        if (sportCategoryContainer.style.display === 'none' || sportCategoryContainer.style.display === '') {
            showSportCategoryContainer(bongRoItem, 'get_category/bongro', 'Bóng Rổ', sportCategoryContainer);
        } else {
            sportCategoryContainer.style.display = 'none';
        }
    });

    pickleballItem.addEventListener('click', function(e) {
        e.stopPropagation();
        if (sportCategoryContainer.style.display === 'none' || sportCategoryContainer.style.display === '') {
            showSportCategoryContainer(pickleballItem, 'get_category/pickeball', 'Pickleball', sportCategoryContainer);
        } else {
            sportCategoryContainer.style.display = 'none';
        }
    });

    cauLongItem.addEventListener('click', function(e) {
        e.stopPropagation();
        if (sportCategoryContainer.style.display === 'none' || sportCategoryContainer.style.display === '') {
            showSportCategoryContainer(cauLongItem, 'get_category/caulong', 'Cầu Lông', sportCategoryContainer);
        } else {
            sportCategoryContainer.style.display = 'none';
        }
    });

    bongChuyenItem.addEventListener('click', function(e) {
        e.stopPropagation();
        if (sportCategoryContainer.style.display === 'none' || sportCategoryContainer.style.display === '') {
            showSportCategoryContainer(bongChuyenItem, 'get_category/bongchuyen', 'Bóng Chuyền', sportCategoryContainer);
        } else {
            sportCategoryContainer.style.display = 'none';
        }
    });

    function showCategoryContainer(menuItem, apiEndpoint) {
        categoryContainer.style.top = menuItem.offsetHeight + 'px';
        categoryContainer.style.left = menuItem.offsetLeft + 'px';
        
        categoryContainer.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 8px;"><i class="fas fa-spinner fa-spin"></i></div>`;
        categoryContainer.style.display = 'grid';
        
        fetch(`/api/${apiEndpoint}`)
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
                    
                    // Xác định ID danh mục
                    const categoryId = category.id_category;
                    catDiv.dataset.id = categoryId;
                    
                    // Xác định tên danh mục
                    const categoryName = category.category_name;
                    catDiv.textContent = categoryName;
                    
                    // Hiển thị số lượng sản phẩm nếu có
                    if (category.product_count !== undefined) {
                        const countSpan = document.createElement('span');
                        countSpan.textContent = ` (${category.product_count})`;
                        countSpan.style.fontSize = '0.8em';
                        countSpan.style.color = '#777';
                        catDiv.appendChild(countSpan);
                    }
                    
                    // Style cho item danh mục
                    Object.assign(catDiv.style, {
                        padding: '8px',
                        cursor: 'pointer',
                        textAlign: 'left',
                        borderRadius: '4px',
                        backgroundColor: '#f9f9f9',
                        transition: 'background-color 0.3s'
                    });
                    
                    // Hiệu ứng hover
                    catDiv.addEventListener('mouseenter', function() {
                        catDiv.style.backgroundColor = '#e0e0e0';
                    });
                    
                    catDiv.addEventListener('mouseleave', function() {
                        catDiv.style.backgroundColor = '#f9f9f9';
                    });
                    
                    // Chuyển hướng khi click vào danh mục
                    catDiv.addEventListener('click', function() {
                        window.location.href = `/list-category/${encodeURIComponent(categoryId)}`;
                    });
                    
                    categoryContainer.appendChild(catDiv);
                });
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
                categoryContainer.innerHTML = `<div style="grid-column: 1 / -1; text-align: center; padding: 8px; color: red;"><i class="fas fa-exclamation-circle"></i> Lỗi tải danh mục.</div>`;
            });
    }
    
    // Hàm hiển thị container danh mục thể thao với thiết kế đẹp hơn
    function showSportCategoryContainer(menuItem, apiEndpoint, sportTitle, container) {
        container.style.top = menuItem.offsetHeight + 'px';
        container.style.left = (menuItem.offsetLeft - 150) + 'px'; // Căn chỉnh để đẹp hơn
        
        container.innerHTML = `<div style="text-align: center; padding: 20px;"><i class="fas fa-spinner fa-spin fa-2x"></i></div>`;
        container.style.display = 'block';
        
        fetch(`/api/${apiEndpoint}`)
            .then(response => response.json())
            .then(data => {
                if (!data || data.length === 0) {
                    container.innerHTML = `
                        <div class="sport-header" style="border-bottom: 2px solid #f0f0f0; margin-bottom: 15px; padding-bottom: 10px;">
                            <h3 style="margin: 0; color: #333; font-size: 18px;">${sportTitle}</h3>
                        </div>
                        <div style="text-align: center; padding: 20px; color: #666;">
                            <i class="fas fa-info-circle" style="margin-right: 8px;"></i>Không có danh mục nào.
                        </div>`;
                    return;
                }
                
                // Tạo header cho container
                let htmlContent = `
                    <div class="sport-header" style="border-bottom: 2px solid #f0f0f0; margin-bottom: 15px; padding-bottom: 10px;">
                        <h3 style="margin: 0; color: #333; font-size: 18px;">${sportTitle}</h3>
                        <div style="font-size: 14px; color: #777; margin-top: 5px;">Tìm thấy ${data.length} danh mục</div>
                    </div>
                    <div class="category-list" style="display: flex; flex-wrap: wrap; gap: 12px;">`;
                
                // Thêm các danh mục vào container
                data.forEach(category => {
                    const categoryName = category.category_name;
                    const categoryId = category.id_category;
                    const productCount = category.product_count !== undefined ? category.product_count : 0;
                    
                    htmlContent += `
                        <div class="sport-category-item" 
                             data-id="${categoryId}" 
                             style="background-color: #f8f9fa; 
                                    border-radius: 6px; 
                                    padding: 12px 15px; 
                                    cursor: pointer; 
                                    transition: all 0.2s ease;
                                    box-shadow: 0 1px 3px rgba(0,0,0,0.08);
                                    width: calc(50% - 6px);">
                            <div style="font-weight: 500; color: #333; margin-bottom: 4px;">${categoryName}</div>
                            <div style="display: flex; justify-content: space-between; align-items: center;">
                                <span style="font-size: 13px; color: #888;">${productCount} sản phẩm</span>
                                <i class="fas fa-chevron-right" style="font-size: 12px; color: #aaa;"></i>
                            </div>
                        </div>`;
                });
                
                htmlContent += `</div>`;
                container.innerHTML = htmlContent;
                
                // Thêm sự kiện cho các item
                container.querySelectorAll('.sport-category-item').forEach(item => {
                    item.addEventListener('mouseover', function() {
                        this.style.backgroundColor = '#e9ecef';
                        this.style.boxShadow = '0 3px 6px rgba(0,0,0,0.1)';
                    });
                    
                    item.addEventListener('mouseout', function() {
                        this.style.backgroundColor = '#f8f9fa';
                        this.style.boxShadow = '0 1px 3px rgba(0,0,0,0.08)';
                    });
                    
                    item.addEventListener('click', function() {
                        const categoryId = this.dataset.id;
                        window.location.href = `/list-category/${encodeURIComponent(categoryId)}`;
                    });
                });
            })
            .catch(error => {
                console.error('Error fetching categories:', error);
                container.innerHTML = `
                    <div class="sport-header" style="border-bottom: 2px solid #f0f0f0; margin-bottom: 15px; padding-bottom: 10px;">
                        <h3 style="margin: 0; color: #333; font-size: 18px;">${sportTitle}</h3>
                    </div>
                    <div style="text-align: center; padding: 20px; color: #d9534f;">
                        <i class="fas fa-exclamation-circle" style="margin-right: 8px;"></i>Lỗi tải danh mục.
                    </div>`;
            });
    }

    document.addEventListener('click', function(e) {
        const isNavItem = Array.from(navMenu.querySelectorAll('.nav-item')).some(item => item.contains(e.target));
        
        if (categoryContainer && !categoryContainer.contains(e.target) && !isNavItem) {
            categoryContainer.style.display = 'none';
        }
        
        if (sportCategoryContainer && !sportCategoryContainer.contains(e.target) && !isNavItem) {
            sportCategoryContainer.style.display = 'none';
        }
    });
});