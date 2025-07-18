// Modern JavaScript for Enhanced User Experience

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initializeScrollAnimations();
    initializeProductGridToggle();
    initializeSearchEnhancements();
    initializeSmoothScrolling();
    initializeTooltips();
    initializeFormValidation();
    initializeCartUpdates();
});

// Scroll-triggered animations
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all animated elements
    document.querySelectorAll('.animate-fade-in, .animate-slide-up, .animate-slide-in-right').forEach(el => {
        observer.observe(el);
    });
}

// Product grid view toggle
function initializeProductGridToggle() {
    const gridBtn = document.getElementById('gridView');
    const listBtn = document.getElementById('listView');
    const productContainer = document.querySelector('.products-grid');

    if (gridBtn && listBtn && productContainer) {
        gridBtn.addEventListener('click', () => {
            setGridView(true);
            gridBtn.classList.add('active');
            listBtn.classList.remove('active');
        });

        listBtn.addEventListener('click', () => {
            setGridView(false);
            listBtn.classList.add('active');
            gridBtn.classList.remove('active');
        });
    }
}

function setGridView(isGrid) {
    const products = document.querySelectorAll('.product-item');
    if (products.length === 0) return;
    
    products.forEach(product => {
        if (isGrid) {
            product.className = 'col-md-6 col-lg-4 product-item mb-4';
        } else {
            product.className = 'col-12 product-item mb-3';
            const card = product.querySelector('.card');
            if (card) {
                card.classList.add('d-md-flex', 'flex-md-row');
                const img = card.querySelector('.card-img-top');
                const body = card.querySelector('.card-body');
                if (img && body) {
                    img.style.width = '200px';
                    img.style.height = '200px';
                    img.style.objectFit = 'cover';
                    body.classList.add('flex-grow-1');
                }
            }
        }
    });
}

// Enhanced search functionality
function initializeSearchEnhancements() {
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput) {
        let searchTimeout;
        
        // Add live search feedback
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 0) {
                this.classList.add('search-active');
                
                // Debounced search suggestions (if implemented)
                searchTimeout = setTimeout(() => {
                    // Could implement live search here
                }, 300);
            } else {
                this.classList.remove('search-active');
            }
        });

        // Enhanced search placeholder animation
        const placeholders = [
            'جستجو در محصولات...',
            'نام محصول را وارد کنید...',
            'برند مورد نظر را بیابید...',
            'دسته‌بندی را جستجو کنید...'
        ];
        
        let placeholderIndex = 0;
        setInterval(() => {
            if (document.activeElement !== searchInput) {
                searchInput.placeholder = placeholders[placeholderIndex];
                placeholderIndex = (placeholderIndex + 1) % placeholders.length;
            }
        }, 3000);
    }
}

// Smooth scrolling for anchor links
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Enhanced tooltips
function initializeTooltips() {
    // Add tooltips for rating stars
    document.querySelectorAll('.stars').forEach(starsEl => {
        const rating = starsEl.dataset.rating;
        if (rating) {
            starsEl.title = `امتیاز: ${rating} از 5`;
        }
    });

    // Add tooltips for action buttons
    document.querySelectorAll('.btn').forEach(btn => {
        if (btn.textContent.includes('سبد خرید')) {
            btn.title = 'افزودن به سبد خرید';
        } else if (btn.textContent.includes('مشاهده جزئیات')) {
            btn.title = 'نمایش اطلاعات کامل محصول';
        }
    });
}

// Form validation enhancements
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Validate required fields
            const requiredFields = form.querySelectorAll('[required]');
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('is-invalid');
                    showFieldError(field, 'این فیلد الزامی است');
                } else {
                    field.classList.remove('is-invalid');
                    field.classList.add('is-valid');
                    hideFieldError(field);
                }
                
                // Email validation
                if (field.type === 'email' && field.value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(field.value)) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'آدرس ایمیل معتبر نیست');
                    }
                }
                
                // Phone validation (Iranian format)
                if (field.name === 'phone' && field.value) {
                    const phoneRegex = /^(\+98|0)?9\d{9}$/;
                    if (!phoneRegex.test(field.value.replace(/\s/g, ''))) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'شماره تلفن معتبر نیست');
                    }
                }
                
                // Password confirmation
                if (field.name === 'confirm_password') {
                    const passwordField = form.querySelector('[name="password"]');
                    if (passwordField && field.value !== passwordField.value) {
                        isValid = false;
                        field.classList.add('is-invalid');
                        showFieldError(field, 'تکرار رمز عبور مطابقت ندارد');
                    }
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                // Scroll to first error
                const firstError = form.querySelector('.is-invalid');
                if (firstError) {
                    firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    firstError.focus();
                }
            }
        });
        
        // Real-time validation
        const inputs = form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
            
            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    validateField(this);
                }
            });
        });
    });
}

function validateField(field) {
    let isValid = true;
    
    if (field.hasAttribute('required') && !field.value.trim()) {
        isValid = false;
        showFieldError(field, 'این فیلد الزامی است');
    } else if (field.type === 'email' && field.value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(field.value)) {
            isValid = false;
            showFieldError(field, 'آدرس ایمیل معتبر نیست');
        }
    }
    
    if (isValid) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
        hideFieldError(field);
    } else {
        field.classList.add('is-invalid');
        field.classList.remove('is-valid');
    }
}

function showFieldError(field, message) {
    hideFieldError(field); // Remove existing error
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;
    field.parentNode.appendChild(errorDiv);
}

function hideFieldError(field) {
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Shopping cart functionality
function addToCart(productId, quantity = 1) {
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', quantity);
    
    fetch('/add-to-cart', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            showNotification('محصول به سبد خرید اضافه شد', 'success');
            updateCartBadge(data.cart_count);
            
            // Animate the add to cart button
            const btn = event.target.closest('.btn');
            if (btn) {
                const originalText = btn.innerHTML;
                btn.innerHTML = '<i class="fas fa-check me-2"></i>اضافه شد!';
                btn.classList.add('btn-success');
                btn.disabled = true;
                
                setTimeout(() => {
                    btn.innerHTML = originalText;
                    btn.classList.remove('btn-success');
                    btn.disabled = false;
                }, 2000);
            }
        } else {
            showNotification(data.message || 'خطا در افزودن به سبد خرید', 'error');
        }
    })
    .catch(error => {
        showNotification('خطا در ارتباط با سرور', 'error');
    });
}

// Update cart badge
function updateCartBadge(count) {
    const badge = document.querySelector('.badge');
    if (badge) {
        badge.textContent = count;
        badge.style.animation = 'pulse 0.5s ease';
    }
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        left: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: none;
        border-radius: 12px;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.remove('show');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.remove();
                }
            }, 150);
        }
    }, 5000);
}

// Price formatting utility
function formatPrice(price) {
    return new Intl.NumberFormat('fa-IR').format(price) + ' تومان';
}

// Loading state management
function setLoadingState(element, isLoading = true) {
    if (isLoading) {
        element.disabled = true;
        element.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>در حال پردازش...';
    } else {
        element.disabled = false;
        // Restore original content
    }
}

// Add to favorites functionality
function toggleFavorite(productId) {
    fetch('/toggle-favorite', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: JSON.stringify({ product_id: productId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const heartIcon = event.target.closest('button').querySelector('i');
            if (data.is_favorite) {
                heartIcon.classList.remove('far');
                heartIcon.classList.add('fas', 'text-danger');
                showNotification('به علاقه‌مندی‌ها اضافه شد', 'success');
            } else {
                heartIcon.classList.remove('fas', 'text-danger');
                heartIcon.classList.add('far');
                showNotification('از علاقه‌مندی‌ها حذف شد', 'info');
            }
        }
    })
    .catch(error => {
        showNotification('خطا در عملیات', 'error');
    });
}

// Lazy loading for images
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));
}

// Initialize lazy loading when DOM is ready
document.addEventListener('DOMContentLoaded', initializeLazyLoading);

// Cart update functionality
function initializeCartUpdates() {
    // Update cart badge when items are added
    const addToCartButtons = document.querySelectorAll('.add-to-cart-btn');
    addToCartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Animate cart badge when item is added
            const cartBadge = document.querySelector('.cart-badge');
            if (cartBadge) {
                cartBadge.style.animation = 'none';
                cartBadge.offsetHeight; // Trigger reflow
                cartBadge.style.animation = 'pulse 0.5s ease-out';
            }
        });
    });
}

// Safe element selection to prevent null errors
function safeQuerySelector(selector) {
    try {
        return document.querySelector(selector);
    } catch (error) {
        console.warn('Element not found:', selector);
        return null;
    }
}

// Replace direct element access with safe selection
function initializeProductGridToggle() {
    const gridBtn = safeQuerySelector('#gridView');
    const listBtn = safeQuerySelector('#listView');
    const productContainer = safeQuerySelector('.products-grid');

    if (gridBtn && listBtn && productContainer) {
        gridBtn.addEventListener('click', () => {
            setGridView(true);
            gridBtn.classList.add('active');
            listBtn.classList.remove('active');
        });

        listBtn.addEventListener('click', () => {
            setGridView(false);
            listBtn.classList.add('active');
            gridBtn.classList.remove('active');
        });
    }
}

// Mobile-specific optimizations (navbar toggle disabled)
document.addEventListener('DOMContentLoaded', function() {
    // Remove any existing navbar toggle functionality since it's disabled
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarCollapse) {
        // Ensure navbar is always visible
        navbarCollapse.classList.add('show');
        navbarCollapse.style.display = 'flex';
    }
    
    // Optimize scroll performance on mobile
    let ticking = false;
    function updateScrollPosition() {
        // Throttle scroll events for better performance
        ticking = false;
    }
    
    window.addEventListener('scroll', () => {
        if (!ticking) {
            requestAnimationFrame(updateScrollPosition);
            ticking = true;
        }
    });
    
    // Touch gesture improvements
    if ('ontouchstart' in window) {
        // Add touch feedback for cards
        const cards = document.querySelectorAll('.card, .btn');
        cards.forEach(card => {
            card.addEventListener('touchstart', function() {
                this.style.transform = 'scale(0.98)';
            });
            
            card.addEventListener('touchend', function() {
                setTimeout(() => {
                    this.style.transform = '';
                }, 150);
            });
        });
    }
    
    // Optimize images for mobile
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('load', function() {
            this.style.opacity = '1';
        });
        
        // Add loading placeholder
        img.style.opacity = '0';
        img.style.transition = 'opacity 0.3s ease';
    });
    
    // Mobile-specific search enhancements
    const searchInput = document.querySelector('input[name="search"]');
    if (searchInput && window.innerWidth < 768) {
        searchInput.addEventListener('focus', function() {
            // Scroll to search input on mobile
            setTimeout(() => {
                this.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 300);
        });
    }
    
    // Back to top functionality
    const backToTopBtn = document.getElementById('backToTop');
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 100) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Newsletter form handling
    const newsletterForm = document.querySelector('.newsletter-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.querySelector('input[type="email"]').value;
            
            if (email) {
                showNotification('با موفقیت در خبرنامه عضو شدید', 'success');
                this.reset();
            }
        });
    }
});