"""
Database models for Persian Bodybuilding Supplements E-commerce Store
"""
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from werkzeug.security import generate_password_hash, check_password_hash


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    """User model for authentication and user management"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    postal_code = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('Order', backref='user', lazy=True)
    
    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash"""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'id': str(self.id),
            'email': self.email,
            'full_name': self.full_name,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'postal_code': self.postal_code,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    """Product category model"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))  # Font Awesome icon class
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True)
    
    def to_dict(self):
        """Convert category to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'icon': self.icon
        }


class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    discount_price = db.Column(db.Numeric(10, 2))
    stock = db.Column(db.Integer, default=0)
    weight = db.Column(db.String(50))  # e.g., "2.5 کیلوگرم"
    brand = db.Column(db.String(100))
    flavor = db.Column(db.String(100))
    image_url = db.Column(db.String(500))
    additional_images = db.Column(db.Text)  # JSON string of image URLs
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    review_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='product', lazy=True)
    
    def get_discount_percentage(self):
        """Calculate discount percentage"""
        if self.discount_price and self.price > self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def get_final_price(self):
        """Get final price (discount price if available, otherwise regular price)"""
        return self.discount_price if self.discount_price else self.price
    
    def to_dict(self):
        """Convert product to dictionary"""
        return {
            'id': str(self.id),
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'discount_price': float(self.discount_price) if self.discount_price else None,
            'stock': self.stock,
            'weight': self.weight,
            'brand': self.brand,
            'flavor': self.flavor,
            'image_url': self.image_url,
            'additional_images': self.additional_images,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'rating': self.rating,
            'review_count': self.review_count,
            'category_id': str(self.category_id),
            'category': self.category.to_dict() if self.category else None,
            'discount_percentage': self.get_discount_percentage(),
            'final_price': float(self.get_final_price())
        }


class Order(db.Model):
    """Order model"""
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    status = db.Column(db.String(20), default='pending', nullable=False)  # pending, confirmed, shipped, delivered, cancelled
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_cost = db.Column(db.Numeric(10, 2), default=0)
    payment_method = db.Column(db.String(50))  # card, cash_on_delivery
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed
    
    # Shipping Information
    shipping_name = db.Column(db.String(100), nullable=False)
    shipping_phone = db.Column(db.String(20), nullable=False)
    shipping_address = db.Column(db.Text, nullable=False)
    shipping_city = db.Column(db.String(50), nullable=False)
    shipping_postal_code = db.Column(db.String(20), nullable=False)
    
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def generate_order_number(self):
        """Generate unique order number"""
        import random
        import string
        while True:
            order_number = ''.join(random.choices(string.digits, k=10))
            if not Order.query.filter_by(order_number=order_number).first():
                return order_number
    
    def get_total_items(self):
        """Get total number of items in order"""
        return sum(item.quantity for item in self.order_items)
    
    def to_dict(self):
        """Convert order to dictionary"""
        return {
            'id': str(self.id),
            'order_number': self.order_number,
            'status': self.status,
            'total_amount': float(self.total_amount),
            'shipping_cost': float(self.shipping_cost),
            'payment_method': self.payment_method,
            'payment_status': self.payment_status,
            'shipping_name': self.shipping_name,
            'shipping_phone': self.shipping_phone,
            'shipping_address': self.shipping_address,
            'shipping_city': self.shipping_city,
            'shipping_postal_code': self.shipping_postal_code,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'user_id': str(self.user_id),
            'items': [item.to_dict() for item in self.order_items],
            'total_items': self.get_total_items()
        }


class OrderItem(db.Model):
    """Order item model"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)  # Price at time of order
    
    # Foreign Keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def get_subtotal(self):
        """Get subtotal for this item"""
        return self.quantity * self.price
    
    def to_dict(self):
        """Convert order item to dictionary"""
        return {
            'id': str(self.id),
            'quantity': self.quantity,
            'price': float(self.price),
            'subtotal': float(self.get_subtotal()),
            'product': self.product.to_dict() if self.product else None
        }