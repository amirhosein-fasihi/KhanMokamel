import json
import os
from typing import List, Dict, Optional

class DataManager:
    """مدیریت داده‌ها با استفاده از فایل‌های JSON"""
    
    def __init__(self):
        self.data_dir = 'data'
        self.ensure_data_dir()
        self.init_data_files()
    
    def ensure_data_dir(self):
        """ایجاد پوشه data در صورت عدم وجود"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
    
    def init_data_files(self):
        """مقداردهی اولیه فایل‌های داده"""
        # Initialize products if not exists
        if not os.path.exists(f'{self.data_dir}/products.json'):
            self.save_data('products.json', [])
        
        # Initialize categories if not exists
        if not os.path.exists(f'{self.data_dir}/categories.json'):
            self.save_data('categories.json', [])
        
        # Initialize orders if not exists
        if not os.path.exists(f'{self.data_dir}/orders.json'):
            self.save_data('orders.json', [])
        
        # Initialize users if not exists
        if not os.path.exists(f'{self.data_dir}/users.json'):
            self.save_data('users.json', [])
    
    def load_data(self, filename: str) -> List[Dict]:
        """بارگذاری داده از فایل JSON"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
    
    def save_data(self, filename: str, data: List[Dict]):
        """ذخیره داده در فایل JSON"""
        filepath = os.path.join(self.data_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    # Product methods
    def get_products(self) -> List[Dict]:
        """دریافت تمام محصولات"""
        return self.load_data('products.json')
    
    def get_product(self, product_id: str) -> Optional[Dict]:
        """دریافت محصول با شناسه"""
        products = self.get_products()
        return next((p for p in products if p['id'] == product_id), None)
    
    def get_featured_products(self, limit: int = 8) -> List[Dict]:
        """دریافت محصولات ویژه"""
        products = self.get_products()
        featured = [p for p in products if p.get('featured', False)]
        return featured[:limit] if featured else products[:limit]
    
    def get_related_products(self, category_id: str, exclude_id: str, limit: int = 4) -> List[Dict]:
        """دریافت محصولات مرتبط"""
        products = self.get_products()
        related = [p for p in products if p.get('category_id') == category_id and p['id'] != exclude_id]
        return related[:limit]
    
    # Category methods
    def get_categories(self) -> List[Dict]:
        """دریافت تمام دسته‌بندی‌ها"""
        return self.load_data('categories.json')
    
    def get_category(self, category_id: str) -> Optional[Dict]:
        """دریافت دسته‌بندی با شناسه"""
        categories = self.get_categories()
        return next((c for c in categories if c['id'] == category_id), None)
    
    # Order methods
    def get_orders(self) -> List[Dict]:
        """دریافت تمام سفارشات"""
        return self.load_data('orders.json')
    
    def add_order(self, order: Dict):
        """افزودن سفارش جدید"""
        orders = self.get_orders()
        orders.append(order)
        self.save_data('orders.json', orders)
    
    def get_user_orders(self, user_id: str) -> List[Dict]:
        """دریافت سفارشات کاربر"""
        orders = self.get_orders()
        return [o for o in orders if o.get('user_id') == user_id]
    
    def update_order_status(self, order_id: str, status: str) -> bool:
        """بروزرسانی وضعیت سفارش"""
        orders = self.get_orders()
        for order in orders:
            if order['id'] == order_id:
                order['status'] = status
                self.save_data('orders.json', orders)
                return True
        return False
    
    # User methods
    def get_users(self) -> List[Dict]:
        """دریافت تمام کاربران"""
        return self.load_data('users.json')
    
    def add_user(self, user: Dict):
        """افزودن کاربر جدید"""
        users = self.get_users()
        users.append(user)
        self.save_data('users.json', users)
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """دریافت کاربر با ایمیل"""
        users = self.get_users()
        return next((u for u in users if u['email'] == email), None)
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict]:
        """دریافت کاربر با شناسه"""
        users = self.get_users()
        return next((u for u in users if u['id'] == user_id), None)
