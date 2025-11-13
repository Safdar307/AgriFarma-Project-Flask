# AgriFarma - Complete Documentation

## 🌾 Project Overview

AgriFarma is a comprehensive Flask-based agricultural platform that combines multiple services for the farming community. It integrates e-commerce, consultation services, discussion forums, and blogging capabilities into a single cohesive application.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone and Setup Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize Database**
   ```bash
   # Apply migrations (if using Flask-Migrate)
   flask db upgrade
   
   # Or create tables directly
   python app.py
   ```

4. **Run Application**
   ```bash
   python app.py
   # OR
   flask run
   ```

5. **Access Application**
   - URL: http://127.0.0.1:5000/
   - Admin Login: admin@agrifarma.com / admin123

## 📁 Project Structure

```
AgriFarma_starter/
├── app.py                 # Main application entry point
├── db.py                 # Database initialization
├── requirements.txt      # Python dependencies
├── utils.py             # Utility functions
├── DOCUMENTATION.md     # This documentation
├── README.md           # Basic project info
├── TODO.md            # Current development tasks
├── migrations/        # Database migration scripts
│   ├── versions/      # Migration files
├── models/           # Database models
│   ├── user.py      # User management
│   ├── product.py   # E-commerce products
│   ├── consultant.py # Consultant profiles
│   ├── post.py      # Blog posts
│   ├── category.py  # Product categories
│   ├── forum.py     # Discussion forum
│   ├── message.py   # User messages
│   ├── blog_*.py    # Blog-related models
│   └── ...
├── routes/           # Application routes
│   ├── auth_routes.py        # Authentication
│   ├── ecommerce_routes.py   # Product management
│   ├── consultancy_routes.py # Consultation services
│   ├── blog_routes.py       # Blog functionality
│   ├── forum_routes.py      # Discussion forum
│   ├── admin_routes.py      # Admin panel
│   └── ...
├── templates/        # Jinja2 templates
│   ├── base.html    # Base template
│   ├── home.html    # Homepage
│   ├── auth/        # Authentication templates
│   ├── ecommerce/   # E-commerce templates
│   ├── blog/        # Blog templates
│   ├── forum/       # Forum templates
│   ├── admin/       # Admin templates
│   └── ...
├── static/          # Static assets
│   ├── css/        # Stylesheets
│   ├── js/         # JavaScript files
│   ├── images/     # Image assets
│   └── uploads/    # User uploaded files
│       ├── avatars/     # Profile pictures
│       ├── products/    # Product images
│       ├── consultants/ # Consultant photos
│       └── ...
├── forms/           # WTForms definitions
├── scripts/         # Utility scripts
├── dev/            # Development tools and docs
└── database/       # SQLite database file
```

## 🏗️ Architecture

### Core Technologies
- **Flask 2.3.3**: Web framework
- **SQLAlchemy 3.0.3**: ORM for database operations
- **Flask-Migrate 4.0.4**: Database migration management
- **Flask-WTF 1.1.1**: Form handling and validation
- **WTForms 3.0.1**: Form validation
- **SQLite**: Database (agrifarma.db)

### Design Patterns
- **Blueprints**: Modular route organization
- **MVC Pattern**: Models, Views, Controllers separation
- **Repository Pattern**: Database operations abstracted in models
- **Template Inheritance**: Base templates with content overrides

## 🔐 Authentication & Authorization

### User Roles
- **User**: Standard user access
- **Admin**: Full administrative privileges
- **Consultant**: Special role for consultation services

### Key Features
- Session-based authentication
- Password hashing with SHA256
- Role-based access control
- Admin-only routes protection

### Default Admin Account
- Email: admin@agrifarma.com
- Password: admin123

## 📊 Database Schema

### Core Tables

#### Users Table
```sql
- id: Primary key
- name: User's full name
- email: Unique email address
- password: Hashed password
- role: User role (user/admin/consultant)
- mobile: Phone number
- location: User location
- profession: User profession
- expertise: Expertise areas
- created_at: Account creation timestamp
```

#### Products Table
```sql
- id: Product ID
- name: Product name
- description: Product description
- price: Product price
- image: Image filename
- active: Product availability status
- category_id: Foreign key to categories
- created_at: Creation timestamp
```

#### Posts Table (Blog)
```sql
- id: Post ID
- title: Post title
- body: Post content
- author_id: Foreign key to users
- category_id: Blog category
- created_at: Creation timestamp
- updated_at: Last modification
- likes_count: Like counter
```

#### Consultants Table
```sql
- id: Consultant ID
- user_id: Foreign key to users
- name: Consultant name
- specialization: Area of expertise
- experience: Years of experience
- description: Profile description
- image: Profile photo
- hourly_rate: Consultation rate
- rating: Average rating
- verified: Verification status
```

### Forum Tables
- **forum_categories**: Discussion categories
- **threads**: Discussion threads
- **replies**: Thread replies

## 🔄 Core Features

### 1. E-Commerce Platform
- **Product Management**: Add, edit, delete products
- **Categories**: Organize products by categories
- **Image Upload**: Product image management
- **Search & Filter**: Find products by name/category

**Routes:**
- `/shop` - Product listing
- `/shop/product/<id>` - Product details
- `/admin/products` - Product management

### 2. Consultation Services
- **Consultant Profiles**: Expert consultant listings
- **Browse Consultants**: Filter by specialization
- **Application System**: Apply to become a consultant
- **Rating System**: Rate and review consultants

**Routes:**
- `/consultancy` - Consultant browsing
- `/consultancy/apply` - Apply to be consultant
- `/admin/consultancy` - Consultant management

### 3. Discussion Forum
- **Categories**: Organize discussions
- **Threads**: Start conversations
- **Replies**: Respond to threads
- **Search**: Find relevant discussions

**Routes:**
- `/forum` - Forum homepage
- `/forum/category/<id>` - Category view
- `/forum/thread/<id>` - Thread view
- `/admin/forum` - Forum management

### 4. Blog System
- **Post Creation**: Rich content publishing
- **Categories & Tags**: Content organization
- **Comments**: Community engagement
- **Likes**: Content appreciation
- **Media Upload**: Images, videos, documents
- **Reply System**: Threaded comments

**Routes:**
- `/blog` - Blog listing
- `/blog/post/<id>` - Individual post
- `/blog/create` - Create new post
- `/admin/blog` - Blog management

### 5. User Management
- **Registration/Login**: Account creation
- **Profiles**: User profile management
- **Role Management**: Admin user control
- **Messages**: Internal messaging system

**Routes:**
- `/auth/login` - User login
- `/auth/register` - User registration
- `/profile` - User profile
- `/admin/users` - User management

### 6. Admin Panel
- **Dashboard**: Admin overview
- **User Management**: Control user accounts
- **Product Management**: E-commerce oversight
- **Content Management**: Blog/forum moderation
- **System Settings**: Application configuration

**Routes:**
- `/admin` - Admin dashboard
- `/admin/users` - User management
- `/admin/products` - Product oversight
- `/admin/messages` - Message center

## 🛠️ Development Tools

### Database Management
```bash
# Apply migrations
flask db upgrade

# Rollback migrations
flask db downgrade

# Generate new migration
flask db migrate -m "Description"
```

### Seed Data Scripts
```bash
# Add dummy products
python dev/seed_dummy_products.py

# Add dummy blog posts
python dev/seed_dummy_blogs.py

# Verify products in database
python dev/verify_products.py

# Fix blog image paths
python dev/fix_blog_images.py
```

### Testing Commands
```bash
# Python shell with Flask context
flask shell

# Check database status
from models.user import User
print(f"Total users: {User.query.count()}")

# View recent products
from models.product import Product
recent = Product.query.order_by(Product.created_at.desc()).limit(5).all()
for p in recent:
    print(f"{p.name} - ${p.price}")
```

## 📋 API Endpoints

### Authentication
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `POST /auth/logout` - User logout

### Blog API
- `GET /blog` - List all posts
- `POST /blog/create` - Create new post
- `GET /blog/post/<id>` - View specific post
- `POST /blog/like/<post_id>` - Like/unlike post
- `POST /blog/comment/<comment_id>/reply` - Reply to comment

### Forum API
- `GET /forum` - List all threads
- `POST /forum/thread` - Create new thread
- `POST /forum/thread/<id>/reply` - Reply to thread

### E-Commerce API
- `GET /shop` - List products
- `GET /shop/product/<id>` - Product details
- `POST /admin/products` - Create product

## 🎨 Frontend Structure

### Template Organization
- **Base Template**: Common layout in `base.html`
- **Page Templates**: Individual page layouts
- **Component Templates**: Reusable UI components
- **Admin Templates**: Administrative interface

### CSS Framework
- **Bootstrap 5**: Responsive design framework
- **Custom Styles**: Agricultural green theme
- **Responsive Design**: Mobile-first approach

### JavaScript Features
- **Form Validation**: Client-side validation
- **AJAX Operations**: Asynchronous requests
- **Interactive UI**: Dynamic content updates

## 📱 User Experience

### Navigation
- **Main Navigation**: Primary site navigation
- **Admin Navigation**: Administrative sidebar
- **Breadcrumbs**: Page hierarchy indication
- **Search Functionality**: Global content search

### Responsive Design
- **Mobile Optimized**: Works on all screen sizes
- **Touch Friendly**: Mobile gesture support
- **Fast Loading**: Optimized assets
- **Offline Support**: Basic offline functionality

## 🔒 Security Features

### Data Protection
- **Password Hashing**: SHA256 encryption
- **CSRF Protection**: Flask-WTF CSRF tokens
- **Input Validation**: Server-side form validation
- **SQL Injection Prevention**: SQLAlchemy ORM

### Access Control
- **Role-Based Permissions**: Different access levels
- **Session Management**: Secure session handling
- **Route Protection**: Admin route decorators
- **File Upload Security**: Controlled file uploads

## 🧪 Testing & Development

### Development Workflow
1. **Code Changes**: Modify source files
2. **Database Updates**: Create migrations
3. **Testing**: Verify functionality
4. **Documentation**: Update docs

### Debugging Tools
- **Flask Debug Mode**: Development server
- **SQLAlchemy Debug**: Database query logging
- **Template Debugging**: Jinja2 error handling

## 📈 Performance Considerations

### Optimization
- **Database Indexing**: Query performance
- **Image Compression**: File size optimization
- **Caching Strategy**: Template and data caching
- **Lazy Loading**: On-demand content loading

### Scalability
- **Modular Architecture**: Easy feature addition
- **Database Design**: Normalized schema
- **File Organization**: Clean directory structure
- **Code Documentation**: Comprehensive docs

## 🚀 Deployment Guide

### Production Setup
1. **Environment Variables**: Set production configs
2. **Database Migration**: Apply all migrations
3. **Static File Serving**: Configure web server
4. **HTTPS Setup**: SSL certificate configuration
5. **Process Management**: Use Gunicorn/WSGI

### Server Requirements
- **Python 3.8+**: Runtime environment
- **Web Server**: Apache/Nginx
- **Database**: SQLite or PostgreSQL
- **File System**: Adequate storage for uploads

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
```bash
# Solution: Check database file permissions
ls -la database/agrifarma.db

# Ensure migrations are applied
flask db upgrade
```

**Template Not Found**
```python
# Solution: Check template directory structure
templates/
├── base.html
├── home.html
└── ...
```

**Import Errors**
```python
# Solution: Verify Python path and imports
import sys
sys.path.append('.')
```

**File Upload Issues**
```python
# Solution: Check upload directory permissions
mkdir -p static/uploads/products
chmod 755 static/uploads/products
```

### Debug Commands
```bash
# Check Flask configuration
flask config

# View application logs
python app.py

# Database shell access
flask shell
from models import *
db.create_all()
```

## 📚 Additional Resources

### Documentation Files
- `dev/BLOG_CREATION_GUIDE.md` - Blog system usage
- `dev/BLOG_QUICK_START.md` - Blog setup guide
- `dev/BLOG_MIGRATION_GUIDE.md` - Database migration details
- `dev/README.md` - Development scripts overview

### Model Documentation
Each model file includes:
- Field definitions and types
- Relationships between tables
- Validation rules
- Custom methods and properties

### Route Documentation
Each route module includes:
- Endpoint definitions
- HTTP methods supported
- Required authentication
- Parameter descriptions

## 🤝 Contributing

### Development Guidelines
1. **Code Style**: Follow PEP 8 standards
2. **Documentation**: Update docs with changes
3. **Testing**: Verify functionality before commit
4. **Migration**: Include database migrations

### Best Practices
- **Modular Design**: Keep features separated
- **Error Handling**: Proper exception management
- **Security**: Validate all inputs
- **Performance**: Optimize queries and assets

## 📞 Support

### Getting Help
- **Documentation**: Review this comprehensive guide
- **Code Comments**: Check inline documentation
- **Error Logs**: Review Flask application logs
- **Database**: Use Flask shell for inspection

### Contact Information
- **Project Repository**: Local development setup
- **Issue Tracking**: Review TODO.md for known issues
- **Feature Requests**: Check existing documentation

---

## 📝 Recent Updates

**November 2025:**
- ✅ Complete blog system implementation
- ✅ Comment reply functionality
- ✅ Like system for posts
- ✅ Enhanced admin panel
- ✅ Mobile-responsive design
- ✅ Database migrations setup

**Next Planned Features:**
- [ ] Dashboard UI improvements (TODO.md)
- [ ] Enhanced search functionality
- [ ] Email notification system
- [ ] Advanced analytics
- [ ] API documentation generation

---

*This documentation covers all aspects of the AgriFarma platform as of November 2025. For the most current information, refer to the source code and inline comments.*