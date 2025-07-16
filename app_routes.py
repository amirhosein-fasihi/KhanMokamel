"""
Route definitions for the Persian Bodybuilding Supplements E-commerce Store
"""
import os
import logging
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import uuid
from database_service import DatabaseService
from utils.auth import login_required, admin_required

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database service
db_service = DatabaseService()

def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/')
    def index():
        """صفحه اصلی فروشگاه"""
        categories = db_service.get_categories()
        featured_products = db_service.get_featured_products()
        return render_template('index.html', categories=categories, products=featured_products)

    @app.route('/products')
    def products():
        """صفحه لیست محصولات"""
        category_id = request.args.get('category')
        search_query = request.args.get('search', '')
        
        # Convert category_id to int if provided
        if category_id:
            try:
                category_id = int(category_id)
            except ValueError:
                category_id = None
        
        # Get products with filtering
        if search_query:
            all_products = db_service.search_products(search_query)
        else:
            all_products = db_service.get_products(category_id=category_id)
        
        categories = db_service.get_categories()
        
        return render_template('products.html', products=all_products, categories=categories, 
                             selected_category=str(category_id) if category_id else None, search_query=search_query)

    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        """صفحه جزئیات محصول"""
        product = db_service.get_product(product_id)
        if not product:
            flash('محصول مورد نظر یافت نشد.', 'error')
            return redirect(url_for('products'))
        
        related_products = db_service.get_related_products(int(product['category_id']), product_id)
        return render_template('product_detail.html', product=product, related_products=related_products)

    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        """افزودن محصول به سبد خرید"""
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity', 1))
        
        product = db_service.get_product(product_id)
        if not product:
            flash('محصول مورد نظر یافت نشد.', 'error')
            return redirect(url_for('products'))
        
        # Initialize cart if not exists
        if 'cart' not in session:
            session['cart'] = {}
        
        # Add or update product in cart (store as string for session compatibility)
        product_id_str = str(product_id)
        if product_id_str in session['cart']:
            session['cart'][product_id_str] += quantity
        else:
            session['cart'][product_id_str] = quantity
        
        session.modified = True
        flash(f'{product["name"]} به سبد خرید اضافه شد.', 'success')
        return redirect(url_for('product_detail', product_id=product_id))

    @app.route('/cart')
    def cart():
        """صفحه سبد خرید"""
        cart_items = []
        total_price = 0
        
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                product = db_service.get_product(int(product_id))
                if product:
                    final_price = product.get('final_price', product['price'])
                    item_total = final_price * quantity
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total': item_total
                    })
                    total_price += item_total
        
        return render_template('cart.html', cart_items=cart_items, total_price=total_price)

    @app.route('/update_cart', methods=['POST'])
    def update_cart():
        """بروزرسانی سبد خرید"""
        product_id = request.form.get('product_id')
        quantity = int(request.form.get('quantity', 0))
        
        if 'cart' in session:
            if quantity > 0:
                session['cart'][product_id] = quantity
            else:
                session['cart'].pop(product_id, None)
            session.modified = True
        
        return redirect(url_for('cart'))

    @app.route('/remove_from_cart/<product_id>')
    def remove_from_cart(product_id):
        """حذف محصول از سبد خرید"""
        if 'cart' in session:
            session['cart'].pop(product_id, None)
            session.modified = True
            flash('محصول از سبد خرید حذف شد.', 'info')
        
        return redirect(url_for('cart'))

    @app.route('/checkout')
    @login_required
    def checkout():
        """صفحه تسویه حساب"""
        cart_items = []
        total_price = 0
        
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                product = db_service.get_product(int(product_id))
                if product:
                    final_price = product.get('final_price', product['price'])
                    item_total = final_price * quantity
                    cart_items.append({
                        'product': product,
                        'quantity': quantity,
                        'total': item_total
                    })
                    total_price += item_total
        
        if not cart_items:
            flash('سبد خرید شما خالی است.', 'error')
            return redirect(url_for('cart'))
        
        return render_template('checkout.html', cart_items=cart_items, total_price=total_price)

    @app.route('/place_order', methods=['POST'])
    @login_required
    def place_order():
        """ثبت سفارش"""
        if 'cart' not in session or not session['cart']:
            flash('سبد خرید شما خالی است.', 'error')
            return redirect(url_for('cart'))
        
        # Get form data
        shipping_info = {
            'shipping_name': request.form.get('shipping_name', session.get('user_name', '')),
            'shipping_phone': request.form.get('shipping_phone'),
            'shipping_address': request.form.get('shipping_address'),
            'shipping_city': request.form.get('shipping_city'),
            'shipping_postal_code': request.form.get('shipping_postal_code'),
            'notes': request.form.get('notes', '')
        }
        payment_method = request.form.get('payment_method', 'cash_on_delivery')
        
        # Prepare cart items for order creation
        cart_items = []
        for product_id, quantity in session['cart'].items():
            cart_items.append({
                'product_id': int(product_id),
                'quantity': quantity
            })
        
        try:
            # Create order using database service
            order = db_service.create_order(
                user_id=int(session['user_id']),
                cart_items=cart_items,
                shipping_info=shipping_info,
                payment_method=payment_method
            )
            
            # Clear cart
            session.pop('cart', None)
            session.modified = True
            
            flash(f'سفارش شما با موفقیت ثبت شد. شماره سفارش: {order["order_number"]}', 'success')
            return redirect(url_for('account'))
            
        except Exception as e:
            logging.error(f"Error placing order: {e}")
            flash('خطا در ثبت سفارش. لطفا دوباره تلاش کنید.', 'error')
            return redirect(url_for('checkout'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """صفحه ورود"""
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = db_service.verify_user_password(email, password)
            if user:
                session['user_id'] = user['id']
                session['user_email'] = user['email']
                session['user_name'] = user['full_name']
                session['is_admin'] = user.get('is_admin', False)
                
                flash('با موفقیت وارد شدید.', 'success')
                return redirect(url_for('index'))
            else:
                flash('ایمیل یا رمز عبور اشتباه است.', 'error')
        
        return render_template('login.html')

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        """صفحه ثبت نام"""
        if request.method == 'POST':
            full_name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            phone = request.form.get('phone', '')
            
            # Validation
            if password != confirm_password:
                flash('رمز عبور و تکرار آن مطابقت ندارند.', 'error')
                return render_template('register.html')
            
            if db_service.get_user_by_email(email):
                flash('این ایمیل قبلاً ثبت شده است.', 'error')
                return render_template('register.html')
            
            try:
                # Create user using database service
                user = db_service.create_user(
                    email=email,
                    password=password,
                    full_name=full_name,
                    phone=phone
                )
                
                flash('ثبت نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.', 'success')
                return redirect(url_for('login'))
                
            except Exception as e:
                logging.error(f"Error creating user: {e}")
                flash('خطا در ثبت نام. لطفا دوباره تلاش کنید.', 'error')
        
        return render_template('register.html')

    @app.route('/logout')
    def logout():
        """خروج از حساب کاربری"""
        session.clear()
        flash('با موفقیت خارج شدید.', 'info')
        return redirect(url_for('index'))

    @app.route('/account')
    @login_required
    def account():
        """صفحه حساب کاربری"""
        user_orders = db_service.get_orders(user_id=int(session['user_id']))
        return render_template('account.html', orders=user_orders)

    @app.route('/admin')
    @admin_required
    def admin():
        """پنل مدیریت"""
        stats = db_service.get_dashboard_stats()
        recent_orders = db_service.get_orders()[:10]  # First 10 orders (most recent due to ORDER BY)
        return render_template('admin.html', stats=stats, recent_orders=recent_orders)

    @app.route('/admin/update_order_status', methods=['POST'])
    @admin_required
    def update_order_status():
        """بروزرسانی وضعیت سفارش"""
        order_id = int(request.form.get('order_id'))
        new_status = request.form.get('status')
        
        if db_service.update_order_status(order_id, new_status):
            flash('وضعیت سفارش بروزرسانی شد.', 'success')
        else:
            flash('خطا در بروزرسانی وضعیت سفارش.', 'error')
        
        return redirect(url_for('admin'))

    @app.errorhandler(404)
    def not_found(error):
        """صفحه 404"""
        return render_template('base.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        """صفحه خطای سرور"""
        return render_template('base.html'), 500