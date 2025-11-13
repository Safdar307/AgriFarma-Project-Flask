from db import db
from datetime import datetime

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category = db.Column(db.String(100))
    category_id = db.Column(db.Integer)
    subcategory_id = db.Column(db.Integer)
    tags = db.Column(db.String(250))

    # Relationships (not adding new columns here to avoid immediate DB change)
    media = db.relationship('BlogMedia', backref='post', cascade='all, delete-orphan')
    comments = db.relationship('BlogComment', backref='post', cascade='all, delete-orphan')
    likes = db.relationship('Like', backref='post_obj', cascade='all, delete-orphan', foreign_keys='Like.post_id')

    def __repr__(self):
        return f'<Post {self.title}>'
