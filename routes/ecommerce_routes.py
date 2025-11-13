from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, jsonify
from db import db
from models.product import Product
from models.cart_item import CartItem
import os
import uuid
from werkzeug.utils import secure_filename
from functools import wraps

ecommerce_bp = Blueprint('ecommerce', __name__, template_folder='../templates/ecommerce')

def login_required(f):
    """Decorator to require login for cart operations"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in to add items to your cart.', 'warning')
            return redirect(url_for('auth.login', next=request.path))
        return f(*args, **kwargs)
    return decorated_function

# Cart helper functions
def get_cart_items():
    """Get cart items for logged in user from database"""
    if not session.get('user_id'):
        return []
    return CartItem.query.filter_by(user_id=session['user_id']).all()

def get_cart_count():
    """Get total number of items in cart"""
    cart_items = get_cart_items()
    return sum(item.quantity for item in cart_items)

def get_cart_total():
    """Get total price of all items in cart"""
    cart_items = get_cart_items()
    total = 0
    for item in cart_items:
        if item.product and item.product.active:
            total += item.product.price * item.quantity
    return total

@ecommerce_bp.route('/cart')
def cart_view():
    """View cart contents"""
    if not session.get('user_id'):
        flash('Please log in to view your cart.', 'warning')
        return redirect(url_for('auth.login'))
    
    cart_items = get_cart_items()
    cart_data = []
    total = 0
    
    for item in cart_items:
        if item.product and item.product.active:
            subtotal = item.product.price * item.quantity
            total += subtotal
            cart_data.append({
                'item': item,
                'product': item.product,
                'quantity': item.quantity,
                'subtotal': subtotal
            })
    
    return render_template('ecommerce/cart.html', cart_items=cart_data, total=total, cart_count=get_cart_count())

@ecommerce_bp.route('/add-to-cart/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    """Add product to cart"""
    try:
        product = Product.query.get_or_404(product_id)
        
        if not product.active:
            flash('Product is not available.', 'error')
            return redirect(url_for('ecommerce.product_detail', product_id=product_id))
        
        quantity = int(request.form.get('quantity', 1))
        
        if quantity <= 0:
            flash('Invalid quantity.', 'error')
            return redirect(url_for('ecommerce.product_detail', product_id=product_id))
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            user_id=session['user_id'],
            product_id=product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(
                user_id=session['user_id'],
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(new_item)
        
        db.session.commit()
        flash(f'Added {quantity} x {product.title} to cart!', 'success')
        
        return redirect(url_for('ecommerce.product_detail', product_id=product_id))
        
    except ValueError:
        flash('Invalid quantity.', 'error')
        return redirect(url_for('ecommerce.product_detail', product_id=product_id))

@ecommerce_bp.route('/add-to-cart/<int:product_id>/ajax', methods=['POST'])
@login_required
def add_to_cart_ajax(product_id):
    """Add product to cart via AJAX"""
    try:
        product = Product.query.get_or_404(product_id)
        
        if not product.active:
            return jsonify({'success': False, 'message': 'Product is not available.'})
        
        quantity = int(request.json.get('quantity', 1)) if request.is_json else 1
        
        if quantity <= 0:
            return jsonify({'success': False, 'message': 'Invalid quantity.'})
        
        # Check if item already exists in cart
        existing_item = CartItem.query.filter_by(
            user_id=session['user_id'],
            product_id=product_id
        ).first()
        
        if existing_item:
            existing_item.quantity += quantity
        else:
            new_item = CartItem(
                user_id=session['user_id'],
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(new_item)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Added {quantity} x {product.title} to cart!',
            'cart_count': get_cart_count()
        })
        
    except ValueError:
        return jsonify({'success': False, 'message': 'Invalid quantity.'})

@ecommerce_bp.route('/update-cart/<int:product_id>', methods=['POST'])
@login_required
def update_cart(product_id):
    """Update quantity of item in cart"""
    try:
        quantity = int(request.form.get('quantity', 1))
        
        cart_item = CartItem.query.filter_by(
            user_id=session['user_id'],
            product_id=product_id
        ).first()
        
        if not cart_item:
            flash('Item not in cart.', 'error')
            return redirect(url_for('ecommerce.cart_view'))
        
        if quantity <= 0:
            # Remove item if quantity is 0 or negative
            db.session.delete(cart_item)
            db.session.commit()
            flash('Item removed from cart.', 'success')
        else:
            # Update quantity
            cart_item.quantity = quantity
            db.session.commit()
            flash('Cart updated.', 'success')
        
        return redirect(url_for('ecommerce.cart_view'))
        
    except ValueError:
        flash('Invalid quantity.', 'error')
        return redirect(url_for('ecommerce.cart_view'))

@ecommerce_bp.route('/remove-from-cart/<int:product_id>', methods=['POST'])
@login_required
def remove_from_cart(product_id):
    """Remove item from cart"""
    cart_item = CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
        flash('Item removed from cart.', 'success')
    else:
        flash('Item not in cart.', 'error')
    
    return redirect(url_for('ecommerce.cart_view'))

@ecommerce_bp.route('/clear-cart', methods=['POST'])
@login_required
def clear_cart():
    """Clear entire cart"""
    CartItem.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()
    flash('Cart cleared.', 'success')
    return redirect(url_for('ecommerce.cart_view'))

@ecommerce_bp.route('/cart-count')
def cart_count():
    """Get cart count for AJAX requests"""
    return jsonify({'count': get_cart_count()})

@ecommerce_bp.route('/')
def product_list():
    q = request.args.get('q', '', type=str).strip()
    sort = request.args.get('sort', 'newest', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    query = Product.query.filter_by(active=True)
    if q:
        like = f"%{q}%"
        query = query.filter((Product.title.ilike(like)) | (Product.description.ilike(like)))

    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'title_asc':
        query = query.order_by(Product.title.asc())
    elif sort == 'title_desc':
        query = query.order_by(Product.title.desc())
    else:
        query = query.order_by(Product.created_at.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('ecommerce/product_list.html', products=pagination.items, pagination=pagination, q=q, sort=sort, per_page=per_page, is_admin=(session.get('user_role')=='admin'))

@ecommerce_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = Product.query.get_or_404(product_id)
    
    # Get related products (simple logic - same category or random products)
    related_products = Product.query.filter(
        Product.id != product.id,
        Product.active == True
    ).limit(4).all()
    
    return render_template('ecommerce/product_detail.html', product=product, related_products=related_products)

@ecommerce_bp.route('/create', methods=['GET','POST'])
def create():
    if session.get('user_role') != 'admin':
        flash('Only admin can create products.', 'error')
        return redirect(url_for('ecommerce.product_list'))
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        price = float(request.form.get('price') or 0)
        active = bool(request.form.get('active'))
        image_path = None
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg','.jpeg','.png','.gif','.webp']:
                unique = f"{uuid.uuid4().hex}{ext}"
                save_path = os.path.join(current_app.config['PRODUCTS_UPLOAD_FOLDER'], unique)
                file.save(save_path)
                image_path = f"uploads/products/{unique}"
        p = Product(title=title, description=description, price=price, active=active, seller_id=session.get('user_id'), image=image_path)
        db.session.add(p)
        db.session.commit()
        flash('Product created.', 'success')
        return redirect(url_for('ecommerce.product_list'))
    return render_template('ecommerce/product_create.html')

@ecommerce_bp.route('/<int:product_id>/edit', methods=['GET','POST'])
def edit(product_id):
    if session.get('user_role') != 'admin':
        flash('Only admin can edit products.', 'error')
        return redirect(url_for('ecommerce.product_list'))
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.title = request.form.get('title', product.title).strip()
        product.description = request.form.get('description', product.description).strip()
        product.price = float(request.form.get('price') or product.price or 0)
        product.active = bool(request.form.get('active'))
        file = request.files.get('image')
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg','.jpeg','.png','.gif','.webp']:
                unique = f"{uuid.uuid4().hex}{ext}"
                save_path = os.path.join(current_app.config['PRODUCTS_UPLOAD_FOLDER'], unique)
                file.save(save_path)
                product.image = f"uploads/products/{unique}"
        db.session.commit()
        flash('Product updated.', 'success')
        return redirect(url_for('ecommerce.product_detail', product_id=product.id))
    return render_template('ecommerce/product_create.html', product=product)

@ecommerce_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete(product_id):
    if session.get('user_role') != 'admin':
        flash('Only admin can delete products.', 'error')
        return redirect(url_for('ecommerce.product_list'))
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('ecommerce.product_list'))
