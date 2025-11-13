# app.py
from flask import Flask, render_template, url_for, session, flash, redirect, request
from flask_migrate import Migrate
from flask_login import LoginManager, current_user
from datetime import datetime
import os
import hashlib
import uuid
from werkzeug.utils import secure_filename

# Import your db instance
from db import db

# Import user model for Flask-Login
from models.user import User

# Import contact form
from forms.contact_form import ContactForm

# Import blueprints
from routes.consultancy_routes import consultancy_bp

# Define filter functions
from datetime import datetime

def timesince(value):
    """
    Returns string representing time since value.
    e.g., "4 minutes ago", "2 hours ago", "3 days ago", etc.
    """
    if not value:
        return ''

    now = datetime.utcnow()
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return value

    diff = now - value
    seconds = diff.total_seconds()

    intervals = [
        ('year', seconds // 31536000),  # 365 days
        ('month', seconds // 2592000),   # 30 days
        ('week', seconds // 604800),     # 7 days
        ('day', seconds // 86400),       # 24 hours
        ('hour', seconds // 3600),
        ('minute', seconds // 60),
        ('second', seconds)
    ]

    for interval, count in intervals:
        if count >= 1:
            count = int(count)
            if count == 1:
                return f"1 {interval} ago"
            else:
                return f"{count} {interval}s ago"
    
    return 'just now'

def nl2br(value):
    """
    Converts newlines to HTML line breaks
    """
    if not value:
        return ''
    
    return value.replace('\n', '<br>')

# =====================================================
# 🚀 Initialize Flask App
# =====================================================
app = Flask(__name__)

# Register custom filters
app.jinja_env.filters['timesince'] = timesince
app.jinja_env.filters['nl2br'] = nl2br

# =====================================================
# ⚙️ Configuration
# =====================================================
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret_key')

# =====================================================
# 🔐 Initialize Flask-Login
# =====================================================
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Base directory of project
basedir = os.path.abspath(os.path.dirname(__file__))

# Ensure database folder exists
os.makedirs(os.path.join(basedir, 'database'), exist_ok=True)

# Database path
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'database', 'agrifarma.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads', 'avatars')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['PRODUCTS_UPLOAD_FOLDER'] = os.path.join(basedir, 'static', 'uploads', 'products')
os.makedirs(app.config['PRODUCTS_UPLOAD_FOLDER'], exist_ok=True)
# Stories feature removed: STORIES_UPLOAD_FOLDER not needed

# Initialize extensions
db.init_app(app)

# --------------------------
# Import models here so migrations can detect them
# --------------------------
try:
    # This ensures SQLAlchemy / Alembic sees your models for autogenerate
    from models import user, post, product, consultant, forum, message
except Exception as e:
    print("⚠️ Warning importing models:", e)

# Now initialize migrations (models are imported above)
migrate = Migrate(app, db)

# =====================================================
# 🕒 Custom Jinja Filter (strftime)
# =====================================================
@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    """Use 'strftime' safely in Jinja2 templates"""
    if isinstance(date, str) and date.lower() == 'now':
        date = datetime.now()
    fmt = fmt or "%B %d, %Y"
    return date.strftime(fmt)

# =====================================================
# 📦 Import Blueprints
# =====================================================
try:
    from routes.auth_routes import auth_bp
    from routes.forum_routes import forum_bp
    from routes.blog_routes import blog_bp
    from routes.ecommerce_routes import ecommerce_bp
    from routes.admin_routes import admin_bp
    from routes.consultancy_routes import consultancy_bp
    from routes.contact_routes import contact_bp

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(forum_bp, url_prefix='/forum')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(ecommerce_bp, url_prefix='/shop')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(consultancy_bp, url_prefix='/consultancy')
    app.register_blueprint(contact_bp)
except ImportError as e:
    print(f"⚠️ Blueprint import error: {e}")

# =====================================================
# 🌐 Routes (kept same as yours)
# =====================================================
@app.route('/')
def home():
    form = ContactForm()
    return render_template('home.html', form=form)

@app.route('/forum')
def forum():
    return redirect(url_for('forum.forum_home'))

@app.route('/blog')
def blog():
    # Redirect to blueprint index
    return redirect(url_for('blog.blog_list'))

@app.route('/consultancy')
def consultancy():
    return redirect(url_for('consultancy.browse_consultants'))

@app.route('/shop')
def shop():
    from models.product import Product
    from models.category import Category
    # Get all active products for the marketplace
    products = Product.query.filter_by(active=True).order_by(Product.created_at.desc()).all()
    categories = Category.query.all()
    return render_template('ecommerce/product_list.html',
                         products=products,
                         pagination=None,
                         q='',
                         sort='newest',
                         per_page=12,
                         is_admin=(session.get('user_role')=='admin'))


@app.route('/stories/')
def stories_home():
    """Placeholder page for Success Stories feature (coming soon)."""
    return render_template('stories/stories.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    form = ContactForm()
    return render_template('contact.html', form=form)

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        flash('Please login to access your profile.', 'warning')
        return redirect(url_for('auth.login'))
    
    # Get user from database
    user = db.session.get(User, session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/edit-profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('user_id'):
        flash('Please login to access your profile.', 'warning')
        return redirect(url_for('auth.login'))
    
    user = db.session.get(User, session['user_id'])
    
    if request.method == 'POST':
        try:
            # Update user information
            user.name = request.form.get('name', '').strip()
            user.email = request.form.get('email', '').strip()
            user.mobile = request.form.get('mobile', '').strip()
            user.location = request.form.get('location', '').strip()
            user.profession = request.form.get('profession', '').strip()
            user.expertise = request.form.get('expertise', '').strip()
            
            # Handle profile picture upload
            file = request.files.get('picture')
            if file and file.filename:
                filename = secure_filename(file.filename)
                ext = os.path.splitext(filename)[1].lower()
                if ext in ['.jpg','.jpeg','.png','.gif','.webp']:
                    # Remove old picture if exists
                    if user.picture:
                        try:
                            old_path = os.path.join('static', user.picture)
                            if os.path.exists(old_path):
                                os.remove(old_path)
                        except Exception as e:
                            print(f"Warning: Could not delete old picture: {e}")
                    
                    # Save new picture
                    unique = f"{uuid.uuid4().hex}{ext}"
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique)
                    file.save(save_path)
                    user.picture = f"uploads/avatars/{unique}"
            
            db.session.commit()
            
            # Update session data
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_picture'] = user.picture
            
            flash('Profile updated successfully!', 'success')
            return redirect(url_for('profile'))
            
        except Exception as e:
            flash('Error updating profile. Please try again.', 'error')
            print(f"Profile update error: {e}")
    
    return render_template('profile.html', user=user, edit_mode=True)



@app.route('/login')
def login():
    return render_template('auth/login.html')

@app.route('/register')
def register():
    return render_template('auth/register.html')

# =====================================================
# 🔧 Context Processors
# =====================================================
@app.context_processor
def inject_cart_data():
    def get_cart_data():
        cart = session.get('cart', {})
        total_items = sum(cart.values()) if cart else 0
        return {'cart_count': total_items, 'cart': cart}
    
    return get_cart_data()

# =====================================================
# 🧠 Database Setup (development convenience)
# =====================================================
if __name__ == '__main__':
    # create tables if they do not exist (safe when using migrations too)
    with app.app_context():
        try:
            db.create_all()
            
            # Create admin user if it doesn't exist
            from models.user import User
            import hashlib
            
            admin_email = "admin@agrifarma.com"
            admin = User.query.filter_by(email=admin_email).first()
            if not admin:
                admin_password = hashlib.sha256("admin123".encode()).hexdigest()
                admin = User(
                    name="Admin",
                    email=admin_email,
                    password=admin_password,
                    role="admin",
                    mobile="03063062307",  # Default mobile number
                    location="AgriFarma HQ",  # Default location
                    profession="Administrator",  # Default profession
                    expertise="System Administration"  # Default expertise
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Admin user created successfully!")
            
        except Exception as e:
            print('❌ Error during DB create_all:', e)

    print(f"Database Path: {os.path.join(basedir, 'database', 'agrifarma.db')}")
    print("Starting AgriFarma Flask App...")
    app.run(debug=True)