import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "fallback-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)  # needed for url_for to generate with https

# configure the database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


def init_sample_data():
    """Initialize database with sample data"""
    from models import Category, Product, User, db
    
    try:
        # Create categories
        categories = [
            {
                'name': 'پروتئین وی',
                'description': 'پروتئین‌های سریع الجذب برای رشد عضله',
                'icon': 'fas fa-dumbbell'
            },
            {
                'name': 'گینر',
                'description': 'مکمل‌های افزایش وزن و حجم عضلانی',
                'icon': 'fas fa-weight'
            },
            {
                'name': 'کراتین',
                'description': 'مکمل‌های افزایش قدرت و انرژی',
                'icon': 'fas fa-bolt'
            },
            {
                'name': 'ویتامین و مواد معدنی',
                'description': 'ویتامین‌ها و مواد معدنی ضروری',
                'icon': 'fas fa-pills'
            },
            {
                'name': 'چربی سوز',
                'description': 'مکمل‌های کاهش وزن و چربی سوزی',
                'icon': 'fas fa-fire'
            },
            {
                'name': 'انرژی و پری ورک اوت',
                'description': 'مکمل‌های افزایش انرژی قبل از تمرین',
                'icon': 'fas fa-rocket'
            }
        ]
        
        category_objects = []
        for cat_data in categories:
            category = Category(**cat_data)
            db.session.add(category)
            category_objects.append(category)
        
        db.session.flush()  # To get category IDs
        
        # Create products
        products = [
            {
                'name': 'پروتئین وی ایرانی پرو',
                'description': 'پروتئین وی عالی برای رشد عضله با طعم شکلات',
                'price': 850000,
                'discount_price': 720000,
                'stock': 50,
                'weight': '2.5 کیلوگرم',
                'brand': 'ایرانی پرو',
                'flavor': 'شکلات',
                'image_url': 'https://cdn.pixabay.com/photo/2017/05/12/11/28/protein-2306687_1280.jpg',
                'is_featured': True,
                'rating': 4.5,
                'review_count': 127,
                'category': category_objects[0]  # پروتئین وی
            },
            {
                'name': 'سیریوس مس گینر',
                'description': 'گینر قوی برای افزایش وزن و حجم عضلانی',
                'price': 1200000,
                'discount_price': 980000,
                'stock': 30,
                'weight': '5 کیلوگرم',
                'brand': 'سیریوس مس',
                'flavor': 'وانیل',
                'image_url': 'https://cdn.pixabay.com/photo/2017/08/26/15/37/fitness-2683044_1280.jpg',
                'is_featured': True,
                'rating': 4.7,
                'review_count': 89,
                'category': category_objects[1]  # گینر
            },
            {
                'name': 'کراتین مونوهیدرات میکرونایز',
                'description': 'کراتین خالص برای افزایش قدرت و انرژی',
                'price': 450000,
                'stock': 75,
                'weight': '300 گرم',
                'brand': 'کیمیا فارما',
                'flavor': 'بی طعم',
                'image_url': 'https://cdn.pixabay.com/photo/2017/08/07/14/02/people-2604149_1280.jpg',
                'is_featured': False,
                'rating': 4.3,
                'review_count': 156,
                'category': category_objects[2]  # کراتین
            },
            {
                'name': 'مولتی ویتامین کامل',
                'description': 'ویتامین‌های کامل روزانه برای ورزشکاران',
                'price': 320000,
                'discount_price': 280000,
                'stock': 100,
                'weight': '60 کپسول',
                'brand': 'ایران داروک',
                'flavor': '',
                'image_url': 'https://cdn.pixabay.com/photo/2017/03/29/04/47/vitamins-2184173_1280.jpg',
                'is_featured': True,
                'rating': 4.1,
                'review_count': 203,
                'category': category_objects[3]  # ویتامین
            },
            {
                'name': 'چربی سوز ترمو',
                'description': 'مکمل قوی چربی سوزی با L-کارنیتین',
                'price': 550000,
                'stock': 40,
                'weight': '90 کپسول',
                'brand': 'فیت لایف',
                'flavor': '',
                'image_url': 'https://cdn.pixabay.com/photo/2017/08/07/14/02/people-2604149_1280.jpg',
                'is_featured': False,
                'rating': 4.0,
                'review_count': 67,
                'category': category_objects[4]  # چربی سوز
            },
            {
                'name': 'پری ورک اوت انرژی بوستر',
                'description': 'انرژی قوی قبل از تمرین با کافئین و آرژنین',
                'price': 380000,
                'discount_price': 340000,
                'stock': 60,
                'weight': '250 گرم',
                'brand': 'انرژی پلاس',
                'flavor': 'آناناس',
                'image_url': 'https://cdn.pixabay.com/photo/2017/05/12/11/28/protein-2306687_1280.jpg',
                'is_featured': True,
                'rating': 4.6,
                'review_count': 94,
                'category': category_objects[5]  # پری ورک اوت
            }
        ]
        
        for prod_data in products:
            product = Product(**prod_data)
            db.session.add(product)
        
        # Create admin user
        admin_user = User(
            email='admin@bodybuilding.ir',
            full_name='مدیر سیستم',
            phone='09123456789',
            is_admin=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Create sample user
        sample_user = User(
            email='user@example.com',
            full_name='علی احمدی',
            phone='09987654321',
            address='تهران، خیابان ولیعصر، پلاک 100',
            city='تهران',
            postal_code='1234567890',
            is_admin=False
        )
        sample_user.set_password('user123')
        db.session.add(sample_user)
        
        db.session.commit()
        print("Sample data initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing sample data: {e}")
        db.session.rollback()


# initialize the app with the extension, flask-sqlalchemy >= 3.0.x
db.init_app(app)

with app.app_context():
    # Make sure to import the models here or their tables won't be created
    import models  # noqa: F401
    
    db.create_all()
    
    # Initialize sample data if tables are empty
    from models import Category, Product, User, Order, OrderItem
    if not Category.query.first():
        init_sample_data()

    # Register routes
    from routes import register_routes
    register_routes(app)