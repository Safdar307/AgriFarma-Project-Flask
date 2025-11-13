from db import db
from datetime import datetime


class BlogMedia(db.Model):
    __tablename__ = 'blog_media'
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    media_type = db.Column(db.String(50))  # image, video, audio, pdf, doc, ppt, other
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BlogMedia {self.media_type}:{self.file_path}>'
"""
Blog media model removed.

Placeholder module kept to indicate blog media was removed during the
redesign. Remove this file entirely when you no longer need a placeholder.
"""



