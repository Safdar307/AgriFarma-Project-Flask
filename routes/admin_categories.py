from flask import render_template, request, redirect, url_for, flash
from db import db
from utils import admin_required

def init_category_routes(admin_bp):
    @admin_bp.route('/categories')
    @admin_required
    def manage_categories():
        from models.category import Category, SubCategory
        categories = Category.query.all()
        return render_template('admin/categories/manage.html', categories=categories)

    @admin_bp.route('/categories/add', methods=['POST'])
    @admin_required
    def add_category():
        from models.category import Category
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        if Category.query.filter_by(name=name).first():
            flash('A category with this name already exists', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully', 'success')
        return redirect(url_for('admin.manage_categories'))

    @admin_bp.route('/categories/<int:id>/edit', methods=['POST'])
    @admin_required
    def edit_category(id):
        from models.category import Category
        category = Category.query.get_or_404(id)
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Category name is required', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        existing = Category.query.filter_by(name=name).first()
        if existing and existing.id != id:
            flash('A category with this name already exists', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        category.name = name
        category.description = description
        db.session.commit()
        flash('Category updated successfully', 'success')
        return redirect(url_for('admin.manage_categories'))

    @admin_bp.route('/categories/<int:id>/delete', methods=['POST'])
    @admin_required
    def delete_category(id):
        from models.category import Category
        category = Category.query.get_or_404(id)
        
        try:
            db.session.delete(category)
            db.session.commit()
            flash('Category deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Cannot delete category as it is being used', 'error')
        
        return redirect(url_for('admin.manage_categories'))

    @admin_bp.route('/categories/<int:category_id>/subcategories/add', methods=['POST'])
    @admin_required
    def add_subcategory(category_id):
        from models.category import Category, SubCategory
        category = Category.query.get_or_404(category_id)
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Subcategory name is required', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        if SubCategory.query.filter_by(name=name, category_id=category_id).first():
            flash('A subcategory with this name already exists in this category', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        subcategory = SubCategory(name=name, description=description, category_id=category_id)
        db.session.add(subcategory)
        db.session.commit()
        flash('Subcategory added successfully', 'success')
        return redirect(url_for('admin.manage_categories'))

    @admin_bp.route('/subcategories/<int:id>/edit', methods=['POST'])
    @admin_required
    def edit_subcategory(id):
        from models.category import SubCategory
        subcategory = SubCategory.query.get_or_404(id)
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Subcategory name is required', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        existing = SubCategory.query.filter_by(name=name, category_id=subcategory.category_id).first()
        if existing and existing.id != id:
            flash('A subcategory with this name already exists in this category', 'error')
            return redirect(url_for('admin.manage_categories'))
        
        subcategory.name = name
        subcategory.description = description
        db.session.commit()
        flash('Subcategory updated successfully', 'success')
        return redirect(url_for('admin.manage_categories'))

    @admin_bp.route('/subcategories/<int:id>/delete', methods=['POST'])
    @admin_required
    def delete_subcategory(id):
        from models.category import SubCategory
        subcategory = SubCategory.query.get_or_404(id)
        
        try:
            db.session.delete(subcategory)
            db.session.commit()
            flash('Subcategory deleted successfully', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Cannot delete subcategory as it is being used', 'error')
        
        return redirect(url_for('admin.manage_categories'))

    return {
        'manage_categories': manage_categories,
        'add_category': add_category,
        'edit_category': edit_category,
        'delete_category': delete_category,
        'add_subcategory': add_subcategory,
        'edit_subcategory': edit_subcategory,
        'delete_subcategory': delete_subcategory
    }