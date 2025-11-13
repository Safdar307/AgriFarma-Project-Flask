from db import db
from datetime import datetime

class CartItem(db.Model):
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('cart_items', lazy='dynamic'))
    product = db.relationship('Product', backref=db.backref('cart_items', lazy='dynamic'))
    
    def __repr__(self):
        return f'<CartItem {self.user_id}: {self.product_id} x{self.quantity}>'
    
    @property
    def subtotal(self):
        return (self.product.price * self.quantity) if self.product else 0