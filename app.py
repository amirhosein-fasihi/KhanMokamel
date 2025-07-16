import os
import json
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from utils.data_manager import DataManager
from utils.auth import login_required, admin_required

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key_change_in_production")
CORS(app)

# Initialize data manager
dm = DataManager()

@app.route('/')
def index():
    """صفحه اصلی فروشگاه"""
    categories = dm.get_categories()
    featured_products = dm.get_featured_products()
    return render_template('index.html', categories=categories, products=featured_products)

@app.route('/products')
def products():
    """صفحه لیست محصولات"""
    category_id = request.args.get('category')
    search_query = request.args.get('search', '')
    
    all_products = dm.get_products()
    categories = dm.get_categories()
    
    # Filter by category
    if category_id:
        all_products = [p for p in all_products if p.get('category_id') == category_id]
    
    # Filter by search query
    if search_query:
        all_products = [p for p in all_products if search_query.lower() in p.get('name', '').lower() or 
                       search_query.lower() in p.get('description', '').lower()]
    
    return render_template('products.html', products=all_products, categories=categories, 
                         selected_category=category_id, search_query=search_query)

@app.route('/product/<product_id>')
def product_detail(product_id):
    """صفحه جزئیات محصول"""
    product = dm.get_product(product_id)
    if not product:
        flash('محصول مورد نظر یافت نشد.', 'error')
        return redirect(url_for('products'))
    
    related_products = dm.get_related_products(product['category_id'], product_id)
    return render_template('product_detail.html', product=product, related_products=related_products)

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    """افزودن محصول به سبد خرید"""
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))
    
    product = dm.get_product(product_id)
    if not product:
        flash('محصول مورد نظر یافت نشد.', 'error')
        return redirect(url_for('products'))
    
    # Initialize cart if not exists
    if 'cart' not in session:
        session['cart'] = {}
    
    # Add or update product in cart
    if product_id in session['cart']:
        session['cart'][product_id] += quantity
    else:
        session['cart'][product_id] = quantity
    
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
            product = dm.get_product(product_id)
            if product:
                item_total = product['price'] * quantity
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
            product = dm.get_product(product_id)
            if product:
                item_total = product['price'] * quantity
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
    shipping_address = request.form.get('shipping_address')
    phone = request.form.get('phone')
    payment_method = request.form.get('payment_method')
    
    # Calculate order total
    total_price = 0
    order_items = []
    
    for product_id, quantity in session['cart'].items():
        product = dm.get_product(product_id)
        if product:
            item_total = product['price'] * quantity
            order_items.append({
                'product_id': product_id,
                'product_name': product['name'],
                'quantity': quantity,
                'price': product['price'],
                'total': item_total
            })
            total_price += item_total
    
    # Create order
    order = {
        'id': str(uuid.uuid4()),
        'user_id': session['user_id'],
        'items': order_items,
        'total_price': total_price,
        'shipping_address': shipping_address,
        'phone': phone,
        'payment_method': payment_method,
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }
    
    dm.add_order(order)
    
    # Clear cart
    session.pop('cart', None)
    session.modified = True
    
    flash('سفارش شما با موفقیت ثبت شد. شماره سفارش: ' + order['id'][:8], 'success')
    return redirect(url_for('account'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """صفحه ورود"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = dm.get_user_by_email(email)
        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            session['user_name'] = user['name']
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
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('رمز عبور و تکرار آن مطابقت ندارند.', 'error')
            return render_template('register.html')
        
        if dm.get_user_by_email(email):
            flash('این ایمیل قبلاً ثبت شده است.', 'error')
            return render_template('register.html')
        
        # Create user
        user = {
            'id': str(uuid.uuid4()),
            'name': name,
            'email': email,
            'password_hash': generate_password_hash(password),
            'is_admin': False,
            'created_at': datetime.now().isoformat()
        }
        
        dm.add_user(user)
        
        flash('ثبت نام با موفقیت انجام شد. اکنون می‌توانید وارد شوید.', 'success')
        return redirect(url_for('login'))
    
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
    user_orders = dm.get_user_orders(session['user_id'])
    return render_template('account.html', orders=user_orders)

@app.route('/admin')
@admin_required
def admin():
    """پنل مدیریت"""
    stats = {
        'total_products': len(dm.get_products()),
        'total_orders': len(dm.get_orders()),
        'total_users': len(dm.get_users()),
        'pending_orders': len([o for o in dm.get_orders() if o['status'] == 'pending'])
    }
    
    recent_orders = dm.get_orders()[-10:]  # Last 10 orders
    return render_template('admin.html', stats=stats, recent_orders=recent_orders)

@app.route('/admin/update_order_status', methods=['POST'])
@admin_required
def update_order_status():
    """بروزرسانی وضعیت سفارش"""
    order_id = request.form.get('order_id')
    new_status = request.form.get('status')
    
    if dm.update_order_status(order_id, new_status):
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
