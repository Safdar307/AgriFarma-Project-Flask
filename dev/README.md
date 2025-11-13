# Development Scripts and Documentation

This folder contains development utilities, dummy data scripts, and documentation for the AgriFarma application.

## Dummy Data Scripts

### Product Management
- **`seed_dummy_products.py`** - Initial seeding of 6 dummy products
- **`add_dummy_products.py`** - Add 6 additional dummy products
- **`verify_products.py`** - Verify products in database

### Blog Management  
- **`seed_dummy_blogs.py`** - Seed dummy blog posts with content
- **`fix_blog_images.py`** - Fix blog media image paths in database
- **`update_blog_images.py`** - Update existing blog posts with correct images

## Documentation

- **`BLOG_CREATION_GUIDE.md`** - Guide for creating blog posts
- **`BLOG_IMPLEMENTATION_COMPLETE.md`** - Complete implementation summary
- **`BLOG_MIGRATION_GUIDE.md`** - Setup and migration instructions  
- **`BLOG_QUICK_START.md`** - Quick start guide for blog features

## Usage

### Running Dummy Data Scripts
```bash
# Product scripts
python dev/seed_dummy_products.py
python dev/add_dummy_products.py
python dev/verify_products.py

# Blog scripts
python dev/seed_dummy_blogs.py
python dev/fix_blog_images.py
python dev/update_blog_images.py
```

### Documentation
Refer to the markdown files for detailed instructions on:
- Blog system setup and migration
- Creating and managing blog posts
- Understanding the blog implementation

## Notes
- These scripts are for development and testing purposes
- All files were moved from the main project directory for better organization
- The application continues to run normally without these files in the main directory
- Updated file paths in scripts to reflect the new location