// Persian-RTL E-commerce Store JavaScript
// Main functionality for bodybuilding supplements store

document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Initialize all components
    initializeNavigation();
    initializeSearch();
    initializeProductFilters();
    initializeCart();
    initializeForms();
    initializeImageGallery();
    initializeModals();
    initializeTooltips();
    initializeScrollEffects();
    initializeLazyLoading();
    
    // Initialize Persian number formatting
    formatPersianNumbers();
    
    // Initialize RTL-specific functionality
    initializeRTLSupport();
}

// Navigation functionality
function initializeNavigation() {
    const navToggler = document.querySelector('.navbar-toggler');
    const navCollapse = document.querySelector('.navbar-collapse');
    
    if (navToggler && navCollapse) {
        navToggler.addEventListener('click', function() {
            navCollapse.classList.toggle('show');
        });
    }
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!event.target.closest('.navbar') && navCollapse && navCollapse.classList.contains('show')) {
            navCollapse.classList.remove('show');
        }
    });
    
    // Active navigation highlighting
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// Search functionality
function initializeSearch() {
    const searchForm = document.querySelector('form[action*="products"]');
    const searchInput = document.querySelector('input[name="search"]');
    
    if (searchForm && searchInput) {
        // Add search suggestions (mock implementation)
        const searchSuggestions = [
            'پروتئین وی',
            'کراتین',
            'گینر',
            'آمینو اسید',
            'پری ورکات',
            'پست ورکات',
            'ویتامین',
            'امگا ۳'
        ];
        
        let suggestionBox = null;
        
        searchInput.addEventListener('input', function() {
            const query = this.value.trim();
            
            if (query.length > 0) {
                showSearchSuggestions(query, searchSuggestions);
            } else {
                hideSearchSuggestions();
            }
        });
        
        searchInput.addEventListener('blur', function() {
            // Delay hiding to allow clicking on suggestions
            setTimeout(hideSearchSuggestions, 200);
        });
        
        function showSearchSuggestions(query, suggestions) {
            const filtered = suggestions.filter(item => 
                item.toLowerCase().includes(query.toLowerCase())
            );
            
            if (filtered.length > 0) {
                if (!suggestionBox) {
                    suggestionBox = document.createElement('div');
                    suggestionBox.className = 'search-suggestions position-absolute bg-white border rounded shadow-lg';
                    suggestionBox.style.cssText = `
                        top: 100%;
                        left: 0;
                        right: 0;
                        z-index: 1000;
                        max-height: 200px;
                        overflow-y: auto;
                    `;
                    searchInput.parentNode.style.position = 'relative';
                    searchInput.parentNode.appendChild(suggestionBox);
                }
                
                suggestionBox.innerHTML = filtered.map(item => 
                    `<div class="suggestion-item p-2 border-bottom cursor-pointer hover:bg-light">${item}</div>`
                ).join('');
                
                // Add click handlers to suggestions
                suggestionBox.querySelectorAll('.suggestion-item').forEach(item => {
                    item.addEventListener('click', function() {
                        searchInput.value = this.textContent;
                        hideSearchSuggestions();
                        searchForm.submit();
                    });
                });
            } else {
                hideSearchSuggestions();
            }
        }
        
        function hideSearchSuggestions() {
            if (suggestionBox) {
                suggestionBox.remove();
                suggestionBox = null;
            }
        }
    }
}

// Product filters functionality
function initializeProductFilters() {
    const filterForm = document.querySelector('.product-filters');
    const priceRange = document.querySelector('#priceRange');
    const categoryFilters = document.querySelectorAll('input[name="category"]');
    const sortSelect = document.querySelector('#sortBy');
    
    if (priceRange) {
        priceRange.addEventListener('input', function() {
            const priceLabel = document.querySelector('#priceLabel');
            if (priceLabel) {
                priceLabel.textContent = formatPrice(this.value);
            }
        });
    }
    
    if (categoryFilters.length > 0) {
        categoryFilters.forEach(filter => {
            filter.addEventListener('change', function() {
                if (filterForm) {
                    filterForm.submit();
                }
            });
        });
    }
    
    if (sortSelect) {
        sortSelect.addEventListener('change', function() {
            if (filterForm) {
                filterForm.submit();
            }
        });
    }
}

// Cart functionality
function initializeCart() {
    const cartButtons = document.querySelectorAll('.add-to-cart');
    const cartQuantityInputs = document.querySelectorAll('.cart-quantity');
    const removeButtons = document.querySelectorAll('.remove-from-cart');
    
    // Add to cart buttons
    cartButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const productId = this.getAttribute('data-product-id');
            const quantity = this.closest('form').querySelector('input[name="quantity"]').value;
            
            addToCart(productId, quantity);
        });
    });
    
    // Cart quantity changes
    cartQuantityInputs.forEach(input => {
        input.addEventListener('change', function() {
            updateCartQuantity(this.getAttribute('data-product-id'), this.value);
        });
    });
    
    // Remove from cart
    removeButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (confirm('آیا مطمئن هستید که می‌خواهید این محصول را از سبد خرید حذف کنید؟')) {
                const productId = this.getAttribute('data-product-id');
                removeFromCart(productId);
            }
        });
    });
    
    // Update cart badge
    updateCartBadge();
}

function addToCart(productId, quantity) {
    // This would typically make an AJAX request
    // For now, we'll use the existing form submission
    const form = document.querySelector(`form[action*="add_to_cart"]`);
    if (form) {
        form.querySelector('input[name="product_id"]').value = productId;
        form.querySelector('input[name="quantity"]').value = quantity;
        form.submit();
    }
}

function updateCartQuantity(productId, quantity) {
    // This would typically make an AJAX request
    const form = document.querySelector(`form[action*="update_cart"]`);
    if (form) {
        form.querySelector('input[name="product_id"]').value = productId;
        form.querySelector('input[name="quantity"]').value = quantity;
        form.submit();
    }
}

function removeFromCart(productId) {
    window.location.href = `/remove_from_cart/${productId}`;
}

function updateCartBadge() {
    const cartBadge = document.querySelector('.cart-badge');
    if (cartBadge) {
        // This would typically get the count from server/localStorage
        const cartItems = JSON.parse(localStorage.getItem('cart') || '{}');
        const totalItems = Object.values(cartItems).reduce((sum, qty) => sum + qty, 0);
        cartBadge.textContent = totalItems;
        cartBadge.style.display = totalItems > 0 ? 'inline' : 'none';
    }
}

// Form validation and enhancement
function initializeForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });
    });
    
    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        input.addEventListener('input', function() {
            showPasswordStrength(this);
        });
    });
    
    // Phone number formatting
    const phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPhoneNumber(this);
        });
    });
    
    // Postal code formatting
    const postalInputs = document.querySelectorAll('input[name="postal_code"]');
    postalInputs.forEach(input => {
        input.addEventListener('input', function() {
            formatPostalCode(this);
        });
    });
}

function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showFieldError(input, 'این فیلد اجباری است');
            isValid = false;
        } else {
            clearFieldError(input);
        }
    });
    
    // Email validation
    const emailInputs = form.querySelectorAll('input[type="email"]');
    emailInputs.forEach(input => {
        if (input.value && !isValidEmail(input.value)) {
            showFieldError(input, 'فرمت ایمیل صحیح نیست');
            isValid = false;
        }
    });
    
    // Phone validation
    const phoneInputs = form.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(input => {
        if (input.value && !isValidPhone(input.value)) {
            showFieldError(input, 'شماره تلفن صحیح نیست');
            isValid = false;
        }
    });
    
    return isValid;
}

function showFieldError(input, message) {
    input.classList.add('is-invalid');
    
    let errorDiv = input.nextElementSibling;
    if (!errorDiv || !errorDiv.classList.contains('invalid-feedback')) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'invalid-feedback';
        input.parentNode.appendChild(errorDiv);
    }
    
    errorDiv.textContent = message;
}

function clearFieldError(input) {
    input.classList.remove('is-invalid');
    
    const errorDiv = input.nextElementSibling;
    if (errorDiv && errorDiv.classList.contains('invalid-feedback')) {
        errorDiv.remove();
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function isValidPhone(phone) {
    const phoneRegex = /^09\d{9}$/;
    return phoneRegex.test(phone.replace(/\D/g, ''));
}

function showPasswordStrength(input) {
    const password = input.value;
    const strength = calculatePasswordStrength(password);
    
    let strengthIndicator = input.parentNode.querySelector('.password-strength');
    if (!strengthIndicator) {
        strengthIndicator = document.createElement('div');
        strengthIndicator.className = 'password-strength mt-1';
        input.parentNode.appendChild(strengthIndicator);
    }
    
    const strengthClasses = ['weak', 'fair', 'good', 'strong'];
    const strengthTexts = ['ضعیف', 'متوسط', 'خوب', 'قوی'];
    
    strengthIndicator.className = `password-strength mt-1 ${strengthClasses[strength]}`;
    strengthIndicator.textContent = `قدرت رمز عبور: ${strengthTexts[strength]}`;
}

function calculatePasswordStrength(password) {
    let strength = 0;
    
    if (password.length >= 8) strength++;
    if (/[a-z]/.test(password)) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;
    
    return Math.min(strength - 1, 3);
}

function formatPhoneNumber(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length > 11) {
        value = value.slice(0, 11);
    }
    
    if (value.length > 3) {
        value = value.slice(0, 3) + '-' + value.slice(3);
    }
    if (value.length > 7) {
        value = value.slice(0, 7) + '-' + value.slice(7);
    }
    
    input.value = value;
}

function formatPostalCode(input) {
    let value = input.value.replace(/\D/g, '');
    
    if (value.length > 10) {
        value = value.slice(0, 10);
    }
    
    input.value = value;
}

// Image gallery functionality
function initializeImageGallery() {
    const mainImage = document.querySelector('#mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail-image');
    
    if (mainImage && thumbnails.length > 0) {
        thumbnails.forEach(thumbnail => {
            thumbnail.addEventListener('click', function() {
                const newSrc = this.src;
                mainImage.src = newSrc;
                
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            });
        });
    }
    
    // Image zoom functionality
    if (mainImage) {
        mainImage.addEventListener('mouseover', function() {
            this.style.cursor = 'zoom-in';
        });
        
        mainImage.addEventListener('click', function() {
            showImageModal(this.src);
        });
    }
}

function showImageModal(imageSrc) {
    const modal = document.createElement('div');
    modal.className = 'image-modal';
    modal.innerHTML = `
        <div class="modal-backdrop" onclick="closeImageModal()"></div>
        <div class="modal-content">
            <img src="${imageSrc}" alt="تصویر بزرگ" class="img-fluid">
            <button class="btn-close" onclick="closeImageModal()">&times;</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    document.body.style.overflow = 'hidden';
}

function closeImageModal() {
    const modal = document.querySelector('.image-modal');
    if (modal) {
        modal.remove();
        document.body.style.overflow = 'auto';
    }
}

// Modal functionality
function initializeModals() {
    const modalTriggers = document.querySelectorAll('[data-bs-toggle="modal"]');
    
    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetModal = document.querySelector(this.getAttribute('data-bs-target'));
            if (targetModal) {
                showModal(targetModal);
            }
        });
    });
    
    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            hideModal(e.target);
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                hideModal(openModal);
            }
        }
    });
}

function showModal(modal) {
    modal.classList.add('show');
    modal.style.display = 'block';
    document.body.style.overflow = 'hidden';
}

function hideModal(modal) {
    modal.classList.remove('show');
    modal.style.display = 'none';
    document.body.style.overflow = 'auto';
}

// Tooltips functionality
function initializeTooltips() {
    const tooltipTriggers = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    
    tooltipTriggers.forEach(trigger => {
        trigger.addEventListener('mouseenter', function() {
            showTooltip(this);
        });
        
        trigger.addEventListener('mouseleave', function() {
            hideTooltip(this);
        });
    });
}

function showTooltip(element) {
    const tooltipText = element.getAttribute('data-bs-title') || element.getAttribute('title');
    
    if (tooltipText) {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip-custom';
        tooltip.textContent = tooltipText;
        
        document.body.appendChild(tooltip);
        
        const rect = element.getBoundingClientRect();
        tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
        tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
        
        element._tooltip = tooltip;
    }
}

function hideTooltip(element) {
    if (element._tooltip) {
        element._tooltip.remove();
        element._tooltip = null;
    }
}

// Scroll effects
function initializeScrollEffects() {
    const scrollElements = document.querySelectorAll('.scroll-animate');
    
    if (scrollElements.length > 0) {
        const observer = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                }
            });
        });
        
        scrollElements.forEach(el => observer.observe(el));
    }
    
    // Back to top button
    const backToTopBtn = document.querySelector('.back-to-top');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.style.display = 'block';
            } else {
                backToTopBtn.style.display = 'none';
            }
        });
        
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
}

// Lazy loading
function initializeLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if (lazyImages.length > 0) {
        const imageObserver = new IntersectionObserver(entries => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    }
}

// Persian number formatting
function formatPersianNumbers() {
    const persianNumbers = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
    const englishNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
    
    const priceElements = document.querySelectorAll('.price, .persian-numbers');
    
    priceElements.forEach(element => {
        let text = element.textContent;
        
        englishNumbers.forEach((num, index) => {
            text = text.replace(new RegExp(num, 'g'), persianNumbers[index]);
        });
        
        element.textContent = text;
    });
}

// RTL-specific functionality
function initializeRTLSupport() {
    // Fix carousel direction for RTL
    const carousels = document.querySelectorAll('.carousel');
    carousels.forEach(carousel => {
        carousel.setAttribute('dir', 'rtl');
    });
    
    // Fix dropdown positioning
    const dropdowns = document.querySelectorAll('.dropdown-menu');
    dropdowns.forEach(dropdown => {
        dropdown.style.left = 'auto';
        dropdown.style.right = '0';
    });
}

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('fa-IR').format(price) + ' تومان';
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('fa-IR');
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        max-width: 400px;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" onclick="this.parentElement.remove()"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Local storage helpers
function saveToLocalStorage(key, value) {
    try {
        localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {
        console.error('Error saving to localStorage:', e);
    }
}

function loadFromLocalStorage(key) {
    try {
        const item = localStorage.getItem(key);
        return item ? JSON.parse(item) : null;
    } catch (e) {
        console.error('Error loading from localStorage:', e);
        return null;
    }
}

// Performance optimization
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export for global use
window.SupplementStore = {
    formatPrice,
    formatDate,
    showNotification,
    saveToLocalStorage,
    loadFromLocalStorage,
    debounce,
    throttle
};
