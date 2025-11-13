from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import db
from models.forum import ForumCategory, Thread, Reply

forum_bp = Blueprint('forum', __name__, template_folder='../templates/discussion_forum')

@forum_bp.route('/')
def forum_home():
    latest_threads = Thread.query.order_by(Thread.created_at.desc()).limit(5).all()
    return render_template('forum_home2.html', latest_threads=latest_threads)

@forum_bp.route('/search')
def forum_search():
    q = request.args.get('q', '').strip()
    if not q:
        return redirect(url_for('forum.forum_home'))
    
    like = f"%{q}%"
    threads = Thread.query.filter(
        (Thread.title.ilike(like)) | (Thread.body.ilike(like))
    ).order_by(Thread.created_at.desc()).all()
    
    categories = ForumCategory.query.all()  # For sidebar navigation
    return render_template('forum_search.html', 
                         threads=threads, 
                         query=q, 
                         categories=categories)

@forum_bp.route('/thread/<int:thread_id>')
def thread_view(thread_id):
    thread = Thread.query.get_or_404(thread_id)
    latest_threads = Thread.query.order_by(Thread.created_at.desc()).limit(5).all()
    related_threads = Thread.query.filter(
        Thread.category_id == thread.category_id,
        Thread.id != thread.id
    ).order_by(Thread.created_at.desc()).limit(5).all()
    categories = ForumCategory.query.all()
    return render_template('thread_view.html', 
                         thread=thread, 
                         latest_threads=latest_threads,
                         related_threads=related_threads,
                         categories=categories)

@forum_bp.route('/category/<int:category_id>')
def category_view(category_id):
    category = ForumCategory.query.get_or_404(category_id)
    latest_threads = Thread.query.order_by(Thread.created_at.desc()).limit(5).all()
    return render_template('category_view.html', 
                         category=category,
                         latest_threads=latest_threads)

@forum_bp.route('/thread/new', methods=['GET','POST'])
def create_thread():
    if not session.get('user_id'):
        flash('Please login to start a discussion.', 'error')
        return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        body = request.form.get('body', '').strip()
        category_id = request.form.get('category_id', type=int)
        
        if not all([title, body, category_id]):
            flash('All fields are required.', 'error')
            categories = ForumCategory.query.all()
            return render_template('create_thread.html', categories=categories)
        
        thread = Thread(
            title=title,
            body=body,
            author_id=session['user_id'],
            category_id=category_id
        )
        db.session.add(thread)
        db.session.commit()
        
        flash('Thread created successfully.', 'success')
        return redirect(url_for('forum.thread_view', thread_id=thread.id))
    
    categories = ForumCategory.query.all()
    return render_template('create_thread.html', categories=categories)

@forum_bp.route('/thread/<int:thread_id>/reply', methods=['POST'])
def add_reply(thread_id):
    if not session.get('user_id'):
        flash('Please login to reply.', 'error')
        return redirect(url_for('auth.login'))
    
    thread = Thread.query.get_or_404(thread_id)
    body = request.form.get('body', '').strip()
    
    if not body:
        flash('Reply cannot be empty.', 'error')
        return redirect(url_for('forum.thread_view', thread_id=thread_id))
    
    reply = Reply(
        body=body,
        author_id=session['user_id'],
        thread_id=thread_id
    )
    db.session.add(reply)
    db.session.commit()
    
    flash('Reply added successfully.', 'success')
    return redirect(url_for('forum.thread_view', thread_id=thread_id))

# Admin: category management, delete/move thread
@forum_bp.route('/admin/categories', methods=['GET','POST'])
def admin_categories():
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('forum.forum_home'))
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        parent_id = request.form.get('parent_id', type=int)
        
        if not name:
            flash('Category name is required.', 'error')
            return redirect(url_for('forum.admin_categories'))
        
        category = ForumCategory(name=name, parent_id=parent_id)
        db.session.add(category)
        db.session.commit()
        
        flash('Category created successfully.', 'success')
        return redirect(url_for('forum.admin_categories'))
    
    categories = ForumCategory.query.all()
    return render_template('admin/forum_categories.html', categories=categories)

@forum_bp.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
def admin_delete_category(category_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('forum.forum_home'))
    
    category = ForumCategory.query.get_or_404(category_id)
    
    # Move threads to parent category if exists
    if category.threads and category.parent_id:
        for thread in category.threads:
            thread.category_id = category.parent_id
    
    db.session.delete(category)
    db.session.commit()
    
    flash('Category deleted successfully.', 'success')
    return redirect(url_for('forum.admin_categories'))

@forum_bp.route('/admin/thread/<int:thread_id>/delete', methods=['POST'])
def admin_delete_thread(thread_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('forum.forum_home'))
    
    thread = Thread.query.get_or_404(thread_id)
    category_id = thread.category_id
    db.session.delete(thread)
    db.session.commit()
    
    flash('Thread deleted successfully.', 'success')
    return redirect(url_for('forum.category_view', category_id=category_id))

@forum_bp.route('/admin/thread/<int:thread_id>/move', methods=['POST'])
def admin_move_thread(thread_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('forum.forum_home'))
    
    thread = Thread.query.get_or_404(thread_id)
    category_id = request.form.get('category_id', type=int)
    
    if not category_id:
        flash('Please select a category.', 'error')
        return redirect(url_for('forum.thread_view', thread_id=thread_id))
    
    thread.category_id = category_id
    db.session.commit()
    
    flash('Thread moved successfully.', 'success')
    return redirect(url_for('forum.thread_view', thread_id=thread_id))

@forum_bp.route('/admin/reply/<int:reply_id>/delete', methods=['POST'])
def admin_delete_reply(reply_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'error')
        return redirect(url_for('forum.forum_home'))
    
    reply = Reply.query.get_or_404(reply_id)
    thread_id = reply.thread_id
    db.session.delete(reply)
    db.session.commit()
    
    flash('Reply deleted successfully.', 'success')
    return redirect(url_for('forum.thread_view', thread_id=thread_id))
