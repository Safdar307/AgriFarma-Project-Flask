#!/usr/bin/env python3
"""
Setup script to populate the database with default agricultural categories and subcategories
for the consultancy application.
"""

import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the app directly from app.py
from app import app
from models.category import Category, SubCategory
from db import db

def setup_consultancy_categories():
    """Create default categories and subcategories for consultancy applications."""
    
    with app.app_context():
        # Define the categories and their subcategories
        categories_data = [
            {
                'name': 'Crop Management',
                'description': 'Expert guidance on crop cultivation, rotation, and harvesting techniques',
                'subcategories': [
                    'Organic Farming',
                    'Conventional Farming',
                    'Sustainable Agriculture',
                    'Crop Rotation Planning',
                    'Harvest Optimization',
                    'Yield Improvement'
                ]
            },
            {
                'name': 'Soil Health & Fertility',
                'description': 'Specialists in soil analysis, nutrient management, and soil conservation',
                'subcategories': [
                    'Soil Testing & Analysis',
                    'Nutrient Management',
                    'Soil Conservation',
                    'Composting Systems',
                    'pH Management',
                    'Organic Matter Management'
                ]
            },
            {
                'name': 'Irrigation & Water Management',
                'description': 'Water system design, conservation, and irrigation technology experts',
                'subcategories': [
                    'Drip Irrigation Systems',
                    'Sprinkler Systems',
                    'Water Conservation',
                    'Rainwater Harvesting',
                    'Irrigation Scheduling',
                    'Precision Agriculture'
                ]
            },
            {
                'name': 'Pest & Disease Management',
                'description': 'Integrated pest management and disease control specialists',
                'subcategories': [
                    'Integrated Pest Management (IPM)',
                    'Biological Control',
                    'Disease Diagnosis',
                    'Pest Identification',
                    'Chemical Control',
                    'Resistance Management'
                ]
            },
            {
                'name': 'Livestock Management',
                'description': 'Animal husbandry, nutrition, and health management experts',
                'subcategories': [
                    'Cattle Management',
                    'Poultry Farming',
                    'Sheep & Goat Farming',
                    'Animal Nutrition',
                    'Veterinary Services',
                    'Breeding Programs'
                ]
            },
            {
                'name': 'Agricultural Technology',
                'description': 'Modern farming technology and digital agriculture specialists',
                'subcategories': [
                    'Precision Agriculture',
                    'GPS & Mapping',
                    'Drone Technology',
                    'IoT in Agriculture',
                    'Farm Management Software',
                    'Weather Monitoring'
                ]
            },
            {
                'name': 'Agricultural Economics',
                'description': 'Farm economics, market analysis, and agricultural business planning',
                'subcategories': [
                    'Farm Business Planning',
                    'Market Analysis',
                    'Financial Planning',
                    'Risk Management',
                    'Supply Chain Management',
                    'Agricultural Policy'
                ]
            },
            {
                'name': 'Greenhouse & Protected Cultivation',
                'description': 'Controlled environment agriculture and greenhouse management',
                'subcategories': [
                    'Greenhouse Design',
                    'Climate Control',
                    'Hydroponic Systems',
                    'Protected Cultivation',
                    'Seedling Production',
                    'Vertical Farming'
                ]
            }
        ]
        
        print("Setting up consultancy categories and subcategories...")
        
        # Check if categories already exist
        existing_categories = Category.query.all()
        if existing_categories:
            print(f"Found {len(existing_categories)} existing categories. Updating...")
            
            # Clear existing categories and subcategories
            SubCategory.query.delete()
            Category.query.delete()
            db.session.commit()
            print("Cleared existing categories and subcategories")
        
        # Create new categories and subcategories
        created_count = 0
        subcategory_count = 0
        
        for cat_data in categories_data:
            # Create category
            category = Category(
                name=cat_data['name'],
                description=cat_data['description']
            )
            db.session.add(category)
            db.session.flush()  # Get the category ID
            
            # Create subcategories
            for subcat_name in cat_data['subcategories']:
                subcategory = SubCategory(
                    name=subcat_name,
                    category_id=category.id,
                    description=f"Specialist in {subcat_name.lower()}"
                )
                db.session.add(subcategory)
                subcategory_count += 1
            
            created_count += 1
            print(f"Created category: {category.name} ({len(cat_data['subcategories'])} subcategories)")
        
        # Commit all changes
        db.session.commit()
        
        print(f"\nSuccessfully created {created_count} categories with {subcategory_count} subcategories!")
        print("\nCategories created:")
        
        # Display the created categories
        categories = Category.query.order_by(Category.name).all()
        for category in categories:
            subcategories = SubCategory.query.filter_by(category_id=category.id).order_by(SubCategory.name).all()
            print(f"\n{category.name}")
            print(f"   {category.description}")
            for subcat in subcategories:
                print(f"   - {subcat.name}")
        
        print("\nSetup complete! Users can now apply as consultants with these categories.")

if __name__ == '__main__':
    setup_consultancy_categories()