from functools import wraps
from flask import session, redirect, url_for, flash

def login_required(f):
    """دکوراتور برای بررسی ورود کاربر"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('برای دسترسی به این صفحه باید وارد شوید.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """دکوراتور برای بررسی دسترسی مدیریت"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('برای دسترسی به این صفحه باید وارد شوید.', 'error')
            return redirect(url_for('login'))
        
        if not session.get('is_admin', False):
            flash('شما دسترسی به این صفحه را ندارید.', 'error')
            return redirect(url_for('index'))
        
        return f(*args, **kwargs)
    return decorated_function
