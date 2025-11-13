"""
Script to add 6 additional dummy products to the ecommerce section
Run with: python add_dummy_products.py
"""

from app import app
from db import db
from models.product import Product
from models.category import Category, SubCategory
from datetime import datetime, timedelta

with app.app_context():
    print("[ADDING] Additional dummy products...")
        
    # Get or create categories for agricultural products
    categories = {}
    category_data = [
        'Seeds & Planting Materials',
        'Tools & Equipment', 
        'Organic Fertilizers',
        'Pest Control Products',
        'Irrigation Equipment',
        'Greenhouse Supplies'
    ]
    
    for cat_name in category_data:
        cat = Category.query.filter_by(name=cat_name).first()
        if not cat:
            cat = Category(name=cat_name, description=f'High quality {cat_name.lower()} for farmers')
            db.session.add(cat)
            db.session.commit()
        categories[cat_name] = cat.id
    
    # Additional dummy products data - 6 agricultural products
    additional_products = [
        {
            'title': 'Organic Heirloom Tomato Seeds',
            'description': 'Premium quality heirloom tomato seeds perfect for home gardening. These seeds produce robust, flavorful tomatoes with excellent disease resistance. Perfect for organic farming and sustainable agriculture.',
            'price': 24.99,
            'category': 'Seeds & Planting Materials',
            'seller_email': 'admin@agrifarma.com',
            'specifications': 'Package: 50 seeds per pack. Germination rate: 95%. Days to maturity: 75-80 days. Sun requirements: Full sun. Soil type: Well-draining, fertile soil.',
            'image': 'https://source.unsplash.com/600x450/?tomato,seeds,organic&sig=1'
        },
        {
            'title': 'Professional Garden Hand Trowel Set',
            'description': 'Heavy-duty stainless steel hand trowel set for professional gardening. Includes 3 different sized trowels with ergonomic wooden handles. Perfect for planting, transplanting, and soil work.',
            'price': 45.50,
            'category': 'Tools & Equipment',
            'seller_email': 'admin@agrifarma.com',
            'specifications': 'Material: Stainless steel blades, wooden handles. Set includes: Small, medium, and large trowels. Weight: 800g total. Warranty: 2 years.',
            'image': './https://source.unsplash.com/600x450/?garden,tools,trowel&sig=2'
        },
        {
            'title': 'Organic Compost Fertilizer (25lbs)',
            'description': 'Rich, organic compost fertilizer made from aged plant materials. Improves soil structure, provides essential nutrients, and promotes healthy plant growth. Ideal for organic farming practices.',
            'price': 32.00,
            'category': 'Organic Fertilizers',
            'seller_email': 'admin@agrifarma.com',
            'specifications': 'Weight: 25 pounds. Organic certified. NPK ratio: 2-1-1. Application rate: 5-10 lbs per 100 sq ft. Coverage: 500-1000 sq ft.',
            'image': 'https://source.unsplash.com/600x450/?compost,fertilizer,organic&sig=3'
        },
        {
            'title': 'Natural Neem Oil Pest Control (500ml)',
            'description': 'Pure neem oil for natural pest control and disease prevention. Effective against aphids, mites, whiteflies, and fungal diseases. Safe for organic farming and beneficial insects.',
            'price': 18.75,
            'category': 'Pest Control Products',
            'seller_email': 'admin@agrifarma.com',
            'specifications': 'Volume: 500ml. Concentration: 100% cold-pressed neem oil. Application: Mix 5-10ml per liter of water. Safe for organic use.',
            'image': 'https://source.unsplash.com/600x450/?neem,oil,pest,control&sig=4'
        },
        {
            'title': 'Drip Irrigation Kit (100 plants)',
            'description': 'Complete drip irrigation system for up to 100 plants. Includes main tubing, emitters, connectors, and timer. Saves water, reduces labor, and promotes uniform plant growth.',
            'price': 129.99,
            'category': 'Irrigation Equipment',
            'seller_email': 'admin@agrifarma.com',
            'specifications': 'Coverage: Up to 100 plants. Pressure rating: 25 PSI. Includes: Timer, main line, drippers, connectors. Warranty: 3 years.',
            'image': 'https://source.unsplash.com/600x450/?drip,irrigation,watering,system&sig=5'
        },
        {
            'title': 'Mini Greenhouse Kit (6x8 feet)',
            'description': 'Portable greenhouse with polycarbonate panels and aluminum frame. Perfect season extension, plant protection, and seed starting. Easy assembly and weather-resistant design.',
            'price': 189.99,
            'category': 'Greenhouse Supplies',
            'seller_email': 'admin@agrifarma.com',
            'specifications': 'Dimensions: 6ft x 8ft x 6.5ft height. Material: Polycarbonate panels, aluminum frame. Doors: 2 sliding doors. Warranty: 5 years.',
            'image': 'https://source.unsplash.com/600x450/?greenhouse,portable,plants&sig=6'
        }
    ]
    
    # Check which products don't exist yet
    existing_titles = [p.title for p in Product.query.all()]
    products_to_create = []
    
    for product_data in additional_products:
        if product_data['title'] not in existing_titles:
            products_to_create.append(product_data)
        else:
            print(f"[SKIPPED] {product_data['title']} (already exists)")
    
    if not products_to_create:
        print("[INFO] All 6 products already exist.")
    else:
        # Create products that don't exist yet
        for i, product_data in enumerate(products_to_create, 1):
            created_at = datetime.utcnow() - timedelta(days=i*2)  # Spread over time
            
            product = Product(
                title=product_data['title'],
                description=product_data['description'],
                price=product_data['price'],
                category_id=categories.get(product_data['category']),
                seller_email=product_data['seller_email'],
                specifications=product_data['specifications'],
                image=product_data['image'],
                active=True,
                created_at=created_at
            )
            
            db.session.add(product)
            print(f"[{i}/{len(products_to_create)}] Created: {product_data['title']}")
        
        db.session.commit()
        print(f"\n[SUCCESS] Created {len(products_to_create)} additional products!")
    
    # Show final count
    total_count = Product.query.count()
    print(f"[INFO] Total products in database: {total_count}")
    print("[INFO] Products are now visible at http://127.0.0.1:5000/ecommerce")