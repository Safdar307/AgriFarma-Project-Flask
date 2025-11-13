from db import db
from datetime import datetime


class CommentReply(db.Model):
    __tablename__ = 'comment_reply'
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(db.Integer, db.ForeignKey('blog_comment.id'), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    author_name = db.Column(db.String(120))
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    comment = db.relationship('BlogComment', backref=db.backref('replies', cascade='all, delete-orphan'))

    def __repr__(self):
        return f'<CommentReply {self.id}>'
