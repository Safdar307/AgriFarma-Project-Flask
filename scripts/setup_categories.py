import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from db import db
from models.forum import ForumCategory

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'database', 'agrifarma.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app

def setup_categories():
    # Define agriculture-related categories
    categories = [
        "Crop Management",
        "Livestock Farming",
        "Agricultural Equipment",
        "Organic Farming",
        "Market & Trade",
        "Farm Technology"
    ]
    
    with create_app().app_context():
        try:
            # Delete any existing categories
            ForumCategory.query.delete()
            
            # Add new categories
            for category_name in categories:
                category = ForumCategory(name=category_name)
                db.session.add(category)
            
            db.session.commit()
            print("Successfully set up forum categories:")
            for cat in categories:
                print(f"- {cat}")
                
        except Exception as e:
            db.session.rollback()
            print(f"Error setting up categories: {e}")

if __name__ == "__main__":
    setup_categories()