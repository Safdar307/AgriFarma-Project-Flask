from db import db
from datetime import datetime


class BlogCategory(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)

    def __repr__(self):
        return f'<BlogCategory {self.name}>'


class BlogSubCategory(db.Model):
    __tablename__ = 'blog_sub_category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'), nullable=False)
    category = db.relationship('BlogCategory', backref='subcategories')

    def __repr__(self):
        return f'<BlogSubCategory {self.name}>'



