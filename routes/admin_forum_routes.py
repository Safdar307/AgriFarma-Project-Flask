from flask import render_template, redirect, url_for, flash, request
from db import db
from models.forum import ForumCategory, Thread
from utils import admin_required

def init_forum_admin_routes(admin_bp):
    @admin_bp.route('/forum')
    @admin_required
    def forum_management():
        # Get all categories with their subcategories using eager loading
        categories = ForumCategory.query.filter_by(parent_id=None).all()
        threads = Thread.query.order_by(Thread.created_at.desc()).limit(20).all()
        return render_template('admin/forum/manage.html', categories=categories, threads=threads)

    @admin_bp.route('/forum/category/add', methods=['POST'])
    @admin_required
    def add_forum_category():
        name = request.form.get('name')
        if name:
            category = ForumCategory(name=name)
            db.session.add(category)
            db.session.commit()
            flash('Category added successfully', 'success')
        else:
            flash('Category name is required', 'error')
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/subcategory/add', methods=['POST'])
    @admin_required
    def add_forum_subcategory():
        name = request.form.get('name')
        parent_id = request.form.get('parent_id', type=int)
        if name and parent_id:
            subcategory = ForumCategory(name=name, parent_id=parent_id)
            db.session.add(subcategory)
            db.session.commit()
            flash('Subcategory added successfully', 'success')
        else:
            flash('Subcategory name and parent category are required', 'error')
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/category/edit', methods=['POST'])
    @admin_required
    def edit_forum_category():
        category_id = request.form.get('category_id', type=int)
        name = request.form.get('name')
        if category_id and name:
            category = ForumCategory.query.get_or_404(category_id)
            category.name = name
            db.session.commit()
            flash('Category updated successfully', 'success')
        else:
            flash('Category ID and name are required', 'error')
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/category/delete', methods=['POST'])
    @admin_required
    def delete_forum_category():
        category_id = request.form.get('category_id', type=int)
        if category_id:
            try:
                category = ForumCategory.query.get_or_404(category_id)
                
                # Check if this category has subcategories
                subcategories = ForumCategory.query.filter_by(parent_id=category_id).all()
                if subcategories:
                    flash('Cannot delete category with existing subcategories. Please delete subcategories first.', 'error')
                    return redirect(url_for('admin.forum_management'))
                
                # Check if there are threads in this category
                threads_count = Thread.query.filter_by(category_id=category_id).count()
                if threads_count > 0:
                    # Delete all threads in this category
                    Thread.query.filter_by(category_id=category_id).delete()
                
                # Delete the category
                db.session.delete(category)
                db.session.commit()
                flash('Category and associated threads deleted successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting category: {str(e)}', 'error')
        else:
            flash('Category ID is required', 'error')
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/subcategory/delete', methods=['POST'])
    @admin_required
    def delete_forum_subcategory():
        subcategory_id = request.form.get('subcategory_id', type=int)
        if subcategory_id:
            try:
                subcategory = ForumCategory.query.get_or_404(subcategory_id)
                
                # Check if there are threads in this subcategory
                threads_count = Thread.query.filter_by(category_id=subcategory_id).count()
                if threads_count > 0:
                    # Delete all threads in this subcategory
                    Thread.query.filter_by(category_id=subcategory_id).delete()
                
                # Delete the subcategory
                db.session.delete(subcategory)
                db.session.commit()
                flash('Subcategory and associated threads deleted successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting subcategory: {str(e)}', 'error')
        else:
            flash('Subcategory ID is required', 'error')
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/thread/move', methods=['POST'])
    @admin_required
    def move_thread():
        thread_id = request.form.get('thread_id', type=int)
        category_id = request.form.get('category_id', type=int)
        if thread_id and category_id:
            thread = Thread.query.get_or_404(thread_id)
            thread.category_id = category_id
            db.session.commit()
            flash('Thread moved successfully', 'success')
        else:
            flash('Thread ID and category ID are required', 'error')
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/thread/delete', methods=['POST'])
    @admin_required
    def delete_thread():
        thread_id = request.form.get('thread_id', type=int)
        if thread_id:
            try:
                thread = Thread.query.get_or_404(thread_id)
                db.session.delete(thread)
                db.session.commit()
                flash('Thread deleted successfully', 'success')
            except Exception as e:
                db.session.rollback()
                flash(f'Error deleting thread: {str(e)}', 'error')
        else:
            flash('Thread ID is required', 'error')
        return redirect(url_for('admin.forum_management'))