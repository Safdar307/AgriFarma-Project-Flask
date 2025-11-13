from flask import Flask
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import db
from models.forum import ForumCategory

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/agrifarma.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'agrifarma.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def setup_forum_categories():
    # Define agriculture-related categories
    categories = [
        "Crop Farming",
        "Livestock Management",
        "Agricultural Equipment",
        "Organic Farming",
        "Market & Trade",
        "Pest Control"
    ]
    
    app = create_app()
    with app.app_context():
        # Clear existing categories
        ForumCategory.query.delete()
        
        # Add new categories
        for category_name in categories:
            category = ForumCategory(name=category_name)
            db.session.add(category)
        
        try:
            db.session.commit()
            print("Successfully set up forum categories!")
            
            # Verify categories were added
            all_categories = ForumCategory.query.all()
            print("\nAvailable categories:")
            for cat in all_categories:
                print(f"- {cat.name}")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error setting up categories: {e}")

if __name__ == "__main__":
    setup_forum_categories()