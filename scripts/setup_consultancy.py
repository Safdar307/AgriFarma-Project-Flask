import os
from app import app, db
from models.category import Category, SubCategory
from models.consultant import Consultant

def setup_database():
    with app.app_context():
        # Create tables
        db.create_all()

        # Add sample categories if none exist
        if not Category.query.first():
            categories = [
                ('Crops', ['Grains', 'Vegetables', 'Fruits', 'Cotton']),
                ('Livestock', ['Cattle', 'Poultry', 'Sheep', 'Goats']),
                ('Farm Management', ['Financial Planning', 'Equipment', 'Labor Management']),
                ('Soil & Irrigation', ['Soil Testing', 'Water Management', 'Fertilization'])
            ]

            for cat_name, subcats in categories:
                category = Category(name=cat_name)
                db.session.add(category)
                db.session.flush()  # Get the ID of the category
                
                for subcat_name in subcats:
                    subcategory = SubCategory(name=subcat_name, category_id=category.id)
                    db.session.add(subcategory)
        
        db.session.commit()

if __name__ == '__main__':
    setup_database()