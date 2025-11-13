from db import db
from datetime import datetime
from sqlalchemy.sql import func

# Categories will be in separate model file

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Float, default=0.0)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    seller_email = db.Column(db.String(200))
    specifications = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    subcategory_id = db.Column(db.Integer, db.ForeignKey('subcategory.id'), nullable=True)
    image = db.Column(db.String(200))

    def __repr__(self):
        return f'<Product {self.title}>'
