"""
Utility script to remove products older than configured days.
Run with the application context (or import and call cleanup_old_products.cleanup()).
"""
from datetime import datetime, timedelta
from db import db
from models.product import Product
from flask import current_app

def cleanup(days=None):
    # days can be passed explicitly, otherwise use app config
    if days is None:
        days = current_app.config.get('PRODUCT_MAX_DAYS', 30)
    cutoff = datetime.utcnow() - timedelta(days=days)
    old = Product.query.filter(Product.created_at < cutoff).all()
    count = len(old)
    for p in old:
        db.session.delete(p)
    db.session.commit()
    return count

if __name__ == '__main__':
    # Running standalone requires an app context; skip when called directly.
    print('This script is intended to be run inside Flask app context.')
