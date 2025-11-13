from flask import render_template, redirect, url_for, flash, request
from db import db
from models.forum import ForumCategory, Thread
from utils import admin_required

def init_forum_admin_routes(admin_bp):
    @admin_bp.route('/forum')
    @admin_required
    def forum_management():
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
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/category/delete', methods=['POST'])
    @admin_required
    def delete_forum_category():
        category_id = request.form.get('category_id', type=int)
        if category_id:
            category = ForumCategory.query.get_or_404(category_id)
            # Delete all threads in this category
            Thread.query.filter_by(category_id=category_id).delete()
            # Delete the category
            db.session.delete(category)
            db.session.commit()
            flash('Category and associated threads deleted successfully', 'success')
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
        return redirect(url_for('admin.forum_management'))

    @admin_bp.route('/forum/thread/delete', methods=['POST'])
    @admin_required
    def delete_thread():
        thread_id = request.form.get('thread_id', type=int)
        if thread_id:
            thread = Thread.query.get_or_404(thread_id)
            db.session.delete(thread)
            db.session.commit()
            flash('Thread deleted successfully', 'success')
        return redirect(url_for('admin.forum_management'))