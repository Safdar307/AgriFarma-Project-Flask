from db import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(50))
    location = db.Column(db.String(200))
    profession = db.Column(db.String(80))
    expertise = db.Column(db.String(80))
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')
    picture = db.Column(db.String(200))
    join_date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.email}>'
