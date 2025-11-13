from db import db
from datetime import datetime


class ForumCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('forum_category.id'))
    parent = db.relationship('ForumCategory', remote_side=[id], backref='children')

    def __repr__(self):
        return f'<ForumCategory {self.name}>'


class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('forum_category.id'), nullable=False)
    category = db.relationship('ForumCategory', backref='threads')
    author = db.relationship('User', backref='threads')

    def __repr__(self):
        return f'<Thread {self.title}>'


class Reply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    thread_id = db.Column(db.Integer, db.ForeignKey('thread.id'), nullable=False)
    thread = db.relationship('Thread', backref='replies')
    author = db.relationship('User', backref='forum_replies')

    def __repr__(self):
        return f'<Reply {self.id}>'



