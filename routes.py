"""
Route definitions for the Persian Bodybuilding Supplements E-commerce Store
"""
import os
import logging
from flask import render_template, request, redirect, url_for, session, flash, jsonify
from datetime import datetime
import uuid
from app import db
from models import User, Category, Product, Order, OrderItem
from utils.auth import login_required, admin_required
from sqlalchemy import func, desc

# Configure logging
logging.basicConfig(level=logging.DEBUG)


def register_routes(app):
    """Register all routes with the Flask app"""
    
    @app.route('/')
    def index():
        """صفحه اصلی فروشگاه"""
        categories = Category.query.all()
        featured_products = Product.query.filter_by(is_featured=True, is_active=True).limit(8).all()
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
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search_query:
            query = query.filter(Product.name.contains(search_query))
        
        all_products = query.all()
        categories = Category.query.all()
        
        return render_template('products.html', products=all_products, categories=categories, 
                             selected_category=str(category_id) if category_id else None, search_query=search_query)

    @app.route('/product/<int:product_id>')
    def product_detail(product_id):
        """صفحه جزئیات محصول"""
        product = Product.query.get_or_404(product_id)
        related_products = (Product.query
                           .filter_by(category_id=product.category_id, is_active=True)
                           .filter(Product.id != product_id)
                           .limit(4)
                           .all())
        return render_template('product_detail.html', product=product, related_products=related_products)

    @app.route('/add_to_cart', methods=['POST'])
    def add_to_cart():
        """افزودن محصول به سبد خرید"""
        product_id = int(request.form.get('product_id'))
        quantity = int(request.form.get('quantity', 1))
        
        product = Product.query.get_or_404(product_id)
        
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
        flash(f'{product.name} به سبد خرید اضافه شد.', 'success')
        return redirect(url_for('product_detail', product_id=product_id))

    @app.route('/cart')
    def cart():
        """صفحه سبد خرید"""
        cart_items = []
        total_price = 0
        
        if 'cart' in session:
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(int(product_id))
                if product:
                    final_price = product.get_final_price()
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
                product = Product.query.get(int(product_id))
                if product:
                    final_price = product.get_final_price()
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
        
        try:
            # Calculate total
            total_amount = 0
            shipping_cost = 50000  # Default shipping cost
            
            # Create order
            order = Order(
                user_id=int(session['user_id']),
                order_number=generate_order_number(),
                total_amount=0,  # Will be updated after adding items
                shipping_cost=shipping_cost,
                payment_method=payment_method,
                **shipping_info
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Add order items
            for product_id, quantity in session['cart'].items():
                product = Product.query.get(int(product_id))
                if product and product.stock >= quantity:
                    # Use current product price or discount price
                    item_price = product.get_final_price()
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=quantity,
                        price=item_price
                    )
                    db.session.add(order_item)
                    
                    # Update product stock
                    product.stock -= quantity
                    
                    total_amount += item_price * quantity
            
            # Update order total
            order.total_amount = total_amount + shipping_cost
            
            db.session.commit()
            
            # Clear cart
            session.pop('cart', None)
            session.modified = True
            
            flash(f'سفارش شما با موفقیت ثبت شد. شماره سفارش: {order.order_number}', 'success')
            return redirect(url_for('account'))
            
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error placing order: {e}")
            flash('خطا در ثبت سفارش. لطفا دوباره تلاش کنید.', 'error')
            return redirect(url_for('checkout'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """صفحه ورود"""
        if request.method == 'POST':
            email = request.form.get('email')
            password = request.form.get('password')
            
            user = User.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['user_name'] = user.full_name
                session['is_admin'] = user.is_admin
                
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
            
            if User.query.filter_by(email=email).first():
                flash('این ایمیل قبلاً ثبت شده است.', 'error')
                return render_template('register.html')
            
            try:
                # Create user
                user = User(
                    email=email,
                    full_name=full_name,
                    phone=phone
                )
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                
                flash('ثبت نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.', 'success')
                return redirect(url_for('login'))
                
            except Exception as e:
                db.session.rollback()
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
        user_orders = Order.query.filter_by(user_id=int(session['user_id'])).order_by(desc(Order.created_at)).all()
        return render_template('account.html', orders=user_orders)

    @app.route('/admin')
    @admin_required
    def admin():
        """پنل مدیریت"""
        total_products = Product.query.filter_by(is_active=True).count()
        total_orders = Order.query.count()
        total_users = User.query.filter_by(is_admin=False).count()
        
        # Calculate total revenue
        total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
        
        stats = {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'total_revenue': float(total_revenue)
        }
        
        recent_orders = Order.query.order_by(desc(Order.created_at)).limit(10).all()
        return render_template('admin.html', stats=stats, recent_orders=recent_orders)

    @app.route('/admin/update_order_status', methods=['POST'])
    @admin_required
    def update_order_status():
        """بروزرسانی وضعیت سفارش"""
        order_id = int(request.form.get('order_id'))
        new_status = request.form.get('status')
        
        order = Order.query.get(order_id)
        if order:
            order.status = new_status
            db.session.commit()
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


def generate_order_number():
    """Generate unique order number"""
    import random
    import string
    while True:
        order_number = ''.join(random.choices(string.digits, k=10))
        if not Order.query.filter_by(order_number=order_number).first():
            return order_number