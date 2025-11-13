from db import db
from datetime import datetime


class BlogComment(db.Model):
    __tablename__ = 'blog_comment'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author_name = db.Column(db.String(120))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogComment {self.id}>'
"""
Blog comment model removed.

This placeholder indicates blog comments were removed for redesign.
"""



