from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app
from db import db
from models.user import User
import os
import uuid
from werkzeug.utils import secure_filename
from models.post import Post
from models.product import Product
from models.consultant import Consultant
from models.forum import ForumCategory, Thread
from utils import admin_required
from routes.admin_forum_routes import init_forum_admin_routes
from routes.admin_categories import init_category_routes

admin_bp = Blueprint('admin', __name__, template_folder='../templates/admin')

# Initialize forum management routes
init_forum_admin_routes(admin_bp)

# Initialize category management routes
category_views = init_category_routes(admin_bp)

@admin_bp.route('/')
@admin_required
def dashboard():
    users = User.query.count()
    posts = Post.query.count()
    products = Product.query.count()
    consultants = Consultant.query.count()
    return render_template('admin/dashboard.html', total_users=users, total_posts=posts, total_products=products, total_consultants=consultants)

@admin_bp.route('/manage_users')
@admin_required
def manage_users():
    q = request.args.get('q', '', type=str).strip()
    role = request.args.get('role', '', type=str).strip()
    sort = request.args.get('sort', 'newest', type=str)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    query = User.query
    if q:
        like = f"%{q}%"
        query = query.filter((User.name.ilike(like)) | (User.email.ilike(like)) | (User.profession.ilike(like)))
    if role:
        query = query.filter(User.role == role)

    if sort == 'name_asc':
        query = query.order_by(User.name.asc())
    elif sort == 'name_desc':
        query = query.order_by(User.name.desc())
    elif sort == 'oldest':
        query = query.order_by(User.join_date.asc())
    else:
        query = query.order_by(User.join_date.desc())

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/manage_users.html', users=pagination.items, pagination=pagination, q=q, role=role, sort=sort, per_page=per_page)

@admin_bp.route('/manage_users/update_role/<int:user_id>', methods=['POST'])
@admin_required
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role', 'user')
    if new_role not in ['user', 'admin']:
        flash('Invalid role selected.', 'error')
        return redirect(url_for('admin.manage_users'))
    user.role = new_role
    db.session.commit()
    flash('User role updated.', 'success')
    return redirect(url_for('admin.manage_users', **request.args))

@admin_bp.route('/manage_users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('User deleted.', 'success')
    return redirect(url_for('admin.manage_users', **request.args))

@admin_bp.route('/manage_users/update/<int:user_id>', methods=['POST'])
@admin_required
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    # Update editable fields
    user.name = request.form.get('name', user.name)
    user.email = request.form.get('email', user.email)
    user.mobile = request.form.get('mobile', user.mobile)
    user.location = request.form.get('location', user.location)
    user.profession = request.form.get('profession', user.profession)
    user.expertise = request.form.get('expertise', user.expertise)
    file = request.files.get('picture')
    if file and file.filename:
        filename = secure_filename(file.filename)
        ext = os.path.splitext(filename)[1].lower()
        if ext in ['.jpg','.jpeg','.png','.gif','.webp']:
            unique = f"{uuid.uuid4().hex}{ext}"
            save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique)
            file.save(save_path)
            user.picture = f"uploads/avatars/{unique}"
    db.session.commit()
    flash('User updated.', 'success')
    return redirect(url_for('admin.manage_users', **request.args))


# ---------------- Admin: Product & Category Management ----------------
@admin_bp.route('/products')
@admin_required
def manage_products():
    q = request.args.get('q', '', type=str).strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)

    query = Product.query
    if q:
        like = f"%{q}%"
        query = query.filter((Product.title.ilike(like)) | (Product.description.ilike(like)))

    query = query.order_by(Product.created_at.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return render_template('admin/products.html', products=pagination.items, pagination=pagination, q=q)


@admin_bp.route('/products/create', methods=['GET','POST'])
@admin_required
def create_product():
    from forms.product_form import ProductForm
    from models.category import Category, SubCategory
    form = ProductForm()
    # populate category choices
    cats = Category.query.order_by(Category.name).all()
    form.category.choices = [(0, '--- Select Category ---')] + [(c.id, c.name) for c in cats]
    form.subcategory.choices = [(0, '--- Select Sub-category ---')]

    if request.method == 'POST' and form.validate_on_submit():
        title = form.title.data.strip()
        description = form.description.data.strip() if form.description.data else ''
        specifications = form.specifications.data or ''
        price = form.price.data or 0
        active = bool(form.active.data)
        seller_email = form.seller_email.data
        category_id = form.category.data or None
        if category_id == 0:
            category_id = None
        subcategory_id = form.subcategory.data or None
        if subcategory_id == 0:
            subcategory_id = None

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

        p = Product(title=title, description=description, specifications=specifications, price=price, active=active, seller_id=session.get('user_id'), seller_email=seller_email, image=image_path, category_id=category_id, subcategory_id=subcategory_id)
        db.session.add(p)
        db.session.commit()
        flash('Product created.', 'success')
        return redirect(url_for('admin.manage_products'))

    return render_template('admin/product_form.html', form=form)


@admin_bp.route('/products/<int:product_id>/edit', methods=['GET','POST'])
@admin_required
def edit_product(product_id):
    from forms.product_form import ProductForm
    from models.category import Category, SubCategory
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    cats = Category.query.order_by(Category.name).all()
    form.category.choices = [(0, '--- Select Category ---')] + [(c.id, c.name) for c in cats]
    subs = SubCategory.query.filter_by(category_id=product.category_id).order_by(SubCategory.name).all() if product.category_id else []
    form.subcategory.choices = [(0, '--- Select Sub-category ---')] + [(s.id, s.name) for s in subs]

    if request.method == 'POST' and form.validate_on_submit():
        product.title = form.title.data.strip()
        product.description = form.description.data or ''
        product.specifications = form.specifications.data or ''
        product.price = form.price.data or 0
        product.active = bool(form.active.data)
        product.seller_email = form.seller_email.data
        category_id = form.category.data or None
        if category_id == 0:
            category_id = None
        product.category_id = category_id
        subcategory_id = form.subcategory.data or None
        if subcategory_id == 0:
            subcategory_id = None
        product.subcategory_id = subcategory_id

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
        return redirect(url_for('admin.manage_products'))

    return render_template('admin/product_form.html', form=form, product=product)


@admin_bp.route('/products/<int:product_id>/delete', methods=['POST'])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted.', 'success')
    return redirect(url_for('admin.manage_products'))


@admin_bp.route('/products/<int:product_id>/toggle', methods=['POST'])
@admin_required
def toggle_product(product_id):
    product = Product.query.get_or_404(product_id)
    product.active = not product.active
    db.session.commit()
    flash('Product status updated.', 'success')
    return redirect(url_for('admin.manage_products'))


@admin_bp.route('/products/cleanup', methods=['POST'])
@admin_required
def cleanup_products():
    from datetime import datetime, timedelta
    days = current_app.config.get('PRODUCT_MAX_DAYS', 30)
    cutoff = datetime.utcnow() - timedelta(days=days)
    old = Product.query.filter(Product.created_at < cutoff).all()
    count = len(old)
    for p in old:
        db.session.delete(p)
    db.session.commit()
    flash(f'Cleanup completed. Removed {count} products older than {days} days.', 'success')
    return redirect(url_for('admin.manage_products'))

