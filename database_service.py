"""
Database service layer for managing data operations
"""
from models import db, User, Category, Product, Order, OrderItem
from typing import List, Optional, Dict
from sqlalchemy import func, desc


class DatabaseService:
    """Service class for database operations"""
    
    @staticmethod
    def get_categories() -> List[Dict]:
        """Get all categories"""
        categories = Category.query.all()
        return [cat.to_dict() for cat in categories]
    
    @staticmethod
    def get_category(category_id: int) -> Optional[Dict]:
        """Get category by ID"""
        category = Category.query.get(category_id)
        return category.to_dict() if category else None
    
    @staticmethod
    def get_products(category_id: Optional[int] = None, search: Optional[str] = None, limit: Optional[int] = None) -> List[Dict]:
        """Get products with optional filtering"""
        query = Product.query.filter_by(is_active=True)
        
        if category_id:
            query = query.filter_by(category_id=category_id)
        
        if search:
            query = query.filter(Product.name.contains(search))
        
        if limit:
            query = query.limit(limit)
        
        products = query.all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_product(product_id: int) -> Optional[Dict]:
        """Get product by ID"""
        product = Product.query.get(product_id)
        return product.to_dict() if product else None
    
    @staticmethod
    def get_featured_products(limit: int = 8) -> List[Dict]:
        """Get featured products"""
        products = Product.query.filter_by(is_featured=True, is_active=True).limit(limit).all()
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_related_products(category_id: int, exclude_id: int, limit: int = 4) -> List[Dict]:
        """Get related products by category"""
        products = (Product.query
                   .filter_by(category_id=category_id, is_active=True)
                   .filter(Product.id != exclude_id)
                   .limit(limit)
                   .all())
        return [product.to_dict() for product in products]
    
    @staticmethod
    def search_products(query: str, limit: int = 20) -> List[Dict]:
        """Search products by name"""
        products = (Product.query
                   .filter(Product.name.contains(query))
                   .filter_by(is_active=True)
                   .limit(limit)
                   .all())
        return [product.to_dict() for product in products]
    
    @staticmethod
    def get_users() -> List[Dict]:
        """Get all users"""
        users = User.query.all()
        return [user.to_dict() for user in users]
    
    @staticmethod
    def get_user_by_email(email: str) -> Optional[Dict]:
        """Get user by email"""
        user = User.query.filter_by(email=email).first()
        return user.to_dict() if user else None
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict]:
        """Get user by ID"""
        user = User.query.get(user_id)
        return user.to_dict() if user else None
    
    @staticmethod
    def create_user(email: str, password: str, full_name: str, **kwargs) -> Dict:
        """Create new user"""
        user = User(
            email=email,
            full_name=full_name,
            **kwargs
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user.to_dict()
    
    @staticmethod
    def verify_user_password(email: str, password: str) -> Optional[Dict]:
        """Verify user password and return user data"""
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            return user.to_dict()
        return None
    
    @staticmethod
    def get_orders(user_id: Optional[int] = None) -> List[Dict]:
        """Get orders, optionally filtered by user"""
        query = Order.query
        if user_id:
            query = query.filter_by(user_id=user_id)
        
        orders = query.order_by(desc(Order.created_at)).all()
        return [order.to_dict() for order in orders]
    
    @staticmethod
    def get_order(order_id: int) -> Optional[Dict]:
        """Get order by ID"""
        order = Order.query.get(order_id)
        return order.to_dict() if order else None
    
    @staticmethod
    def create_order(user_id: int, cart_items: List[Dict], shipping_info: Dict, payment_method: str = 'cash_on_delivery') -> Dict:
        """Create new order"""
        try:
            # Calculate total
            total_amount = 0
            shipping_cost = 50000  # Default shipping cost
            
            # Create order
            order = Order(
                user_id=user_id,
                order_number=Order().generate_order_number(),
                total_amount=0,  # Will be updated after adding items
                shipping_cost=shipping_cost,
                payment_method=payment_method,
                **shipping_info
            )
            db.session.add(order)
            db.session.flush()  # Get order ID
            
            # Add order items
            for item in cart_items:
                product = Product.query.get(item['product_id'])
                if product and product.stock >= item['quantity']:
                    # Use current product price or discount price
                    item_price = product.get_final_price()
                    
                    order_item = OrderItem(
                        order_id=order.id,
                        product_id=product.id,
                        quantity=item['quantity'],
                        price=item_price
                    )
                    db.session.add(order_item)
                    
                    # Update product stock
                    product.stock -= item['quantity']
                    
                    total_amount += item_price * item['quantity']
            
            # Update order total
            order.total_amount = total_amount + shipping_cost
            
            db.session.commit()
            return order.to_dict()
            
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def update_order_status(order_id: int, status: str) -> bool:
        """Update order status"""
        try:
            order = Order.query.get(order_id)
            if order:
                order.status = status
                db.session.commit()
                return True
            return False
        except Exception:
            db.session.rollback()
            return False
    
    @staticmethod
    def get_dashboard_stats() -> Dict:
        """Get dashboard statistics"""
        total_products = Product.query.filter_by(is_active=True).count()
        total_orders = Order.query.count()
        total_users = User.query.filter_by(is_admin=False).count()
        
        # Calculate total revenue
        total_revenue = db.session.query(func.sum(Order.total_amount)).scalar() or 0
        
        return {
            'total_products': total_products,
            'total_orders': total_orders,
            'total_users': total_users,
            'total_revenue': float(total_revenue)
        }