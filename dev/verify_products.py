"""
Script to verify products in database
Run with: python verify_products.py
"""

from app import app
from db import db
from models.product import Product
from models.category import Category

with app.app_context():
    print("=== DATABASE VERIFICATION ===")
    
    # Check categories
    print(f"Total categories: {Category.query.count()}")
    categories = Category.query.all()
    for cat in categories:
        print(f"- Category: {cat.name} (ID: {cat.id})")
    
    print(f"\nTotal products: {Product.query.count()}")
    
    # Check products
    products = Product.query.all()
    if products:
        print("\n=== PRODUCTS FOUND ===")
        for p in products:
            print(f"ID: {p.id}")
            print(f"Title: {p.title}")
            print(f"Price: ${p.price}")
            print(f"Category ID: {p.category_id}")
            print(f"Active: {p.active}")
            print(f"Created: {p.created_at}")
            print("-" * 50)
    else:
        print("\n=== NO PRODUCTS FOUND ===")
        
    # Check if products are active
    active_products = Product.query.filter_by(active=True).count()
    print(f"\nActive products: {active_products}")
    
    print("\n=== TESTING QUERY ===")
    # Test the same query used in the template
    query = Product.query.filter_by(active=True)
    result = query.all()
    print(f"Query result: {len(result)} products")