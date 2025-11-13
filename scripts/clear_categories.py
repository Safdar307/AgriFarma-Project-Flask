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

def clear_categories():
    with create_app().app_context():
        try:
            # Delete all categories
            ForumCategory.query.delete()
            db.session.commit()
            print("Successfully cleared all forum categories!")
        except Exception as e:
            db.session.rollback()
            print(f"Error clearing categories: {e}")

if __name__ == "__main__":
    clear_categories()