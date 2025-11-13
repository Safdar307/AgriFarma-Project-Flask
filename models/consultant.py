from db import db
from datetime import datetime
from models.category import Category

class Consultant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    __table_args__ = (
        db.UniqueConstraint('email', name='uq_consultant_email'),
    )
    phone = db.Column(db.String(20), nullable=False)
    expertise_category = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    bio = db.Column(db.Text, nullable=False)
    profile_picture = db.Column(db.String(255))
    status = db.Column(db.Enum('pending', 'approved', 'rejected', name='consultant_status'), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category_rel = db.relationship('Category', foreign_keys=[expertise_category])

    def __repr__(self):
        return f'<Consultant {self.name}>'
