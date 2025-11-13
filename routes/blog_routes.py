from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_from_directory
from db import db
from models.post import Post
from models.blog_taxonomy import BlogCategory, BlogSubCategory
from models.blog_media import BlogMedia
from models.blog_comment import BlogComment
from models.user import User
from models.like import Like
from models.comment_reply import CommentReply
import os
import uuid
from werkzeug.utils import secure_filename

blog_bp = Blueprint('blog', __name__)

ALLOWED_EXT = set(['.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.webm', '.ogg', '.mp3', '.wav', '.pdf', '.doc', '.docx', '.ppt', '.pptx'])


def allowed_file_ext(filename):
    ext = os.path.splitext(filename)[1].lower()
    return ext in ALLOWED_EXT


def detect_media_type(ext):
    if ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
        return 'image'
    if ext in ['.mp4', '.webm', '.ogg']:
        return 'video'
    if ext in ['.mp3', '.wav']:
        return 'audio'
    if ext in ['.pdf', '.doc', '.docx', '.ppt', '.pptx']:
        return 'document'
    return 'other'


@blog_bp.route('/')
def blog_list():
    q = request.args.get('q', '').strip()
    cat = request.args.get('cat', type=int)
    tag = request.args.get('tag', '').strip()

    query = Post.query
    if cat:
        query = query.filter(Post.category_id == cat)
    if q:
        like = f"%{q}%"
        query = query.filter((Post.title.ilike(like)) | (Post.body.ilike(like)) | (Post.tags.ilike(like)))
    if tag:
        query = query.filter(Post.tags.ilike(f"%{tag}%"))

    posts = query.order_by(Post.created_at.desc()).all()
    categories = BlogCategory.query.order_by(BlogCategory.name.asc()).all()
    latest = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('blog_list.html', posts=posts, categories=categories, latest=latest, q=q, cat=cat)


@blog_bp.route('/<int:post_id>')
def blog_post(post_id):
    post = Post.query.get_or_404(post_id)
    media = BlogMedia.query.filter_by(post_id=post.id).all()
    comments = BlogComment.query.filter_by(post_id=post.id).order_by(BlogComment.created_at.asc()).all()
    latest = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template('blog_post.html', post=post, media=media, comments=comments, latest=latest)


@blog_bp.route('/create', methods=['GET', 'POST'])
def create():
    if not session.get('user_id'):
        flash('Please login to create a post.', 'warning')
        return redirect(url_for('auth.login'))

    categories = BlogCategory.query.order_by(BlogCategory.name.asc()).all()
    subcats = BlogSubCategory.query.all()

    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        category_id = request.form.get('category_id', type=int)
        subcategory_id = request.form.get('subcategory_id', type=int)
        tags = request.form.get('tags', '').strip()
        body = request.form.get('body', '').strip()

        # get category name if available
        category_name = None
        if category_id:
            c = BlogCategory.query.get(category_id)
            category_name = c.name if c else None

        post = Post(title=title, body=body, author_id=session.get('user_id'), category=category_name, category_id=category_id, subcategory_id=subcategory_id, tags=tags)
        db.session.add(post)
        db.session.commit()

        # handle uploads
        for file in request.files.getlist('media'):
            if file and file.filename:
                filename = secure_filename(file.filename)
                ext = os.path.splitext(filename)[1].lower()
                if not allowed_file_ext(filename):
                    continue
                unique = f"{uuid.uuid4().hex}{ext}"
                folder = os.path.join(current_app.root_path, 'static', 'uploads', 'blog')
                os.makedirs(folder, exist_ok=True)
                save_path = os.path.join(folder, unique)
                file.save(save_path)
                media_type = detect_media_type(ext)
                m = BlogMedia(post_id=post.id, file_path=f"uploads/blog/{unique}", media_type=media_type)
                db.session.add(m)
        db.session.commit()

        flash('Post created.', 'success')
        return redirect(url_for('blog.blog_post', post_id=post.id))

    return render_template('blog_create.html', categories=categories, subcats=subcats)


@blog_bp.route('/comment/<int:post_id>', methods=['POST'])
def add_comment(post_id):
    post = Post.query.get_or_404(post_id)
    body = request.form.get('body', '').strip()
    if not body:
        flash('Comment cannot be empty.', 'warning')
        return redirect(url_for('blog.blog_post', post_id=post.id))

    author_id = session.get('user_id')
    author_name = session.get('user_name') or (User.query.get(author_id).name if author_id else 'Anonymous')
    c = BlogComment(post_id=post.id, author_id=author_id, author_name=author_name, body=body)
    db.session.add(c)
    db.session.commit()
    flash('Comment added.', 'success')
    return redirect(url_for('blog.blog_post', post_id=post.id))


# Admin: categories and moderation
@blog_bp.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('blog.blog_list'))
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        parent_id = request.form.get('parent_id', type=int)
        if parent_id:
            sub = BlogSubCategory(name=name, category_id=parent_id)
            db.session.add(sub)
        else:
            cat = BlogCategory(name=name)
            db.session.add(cat)
        db.session.commit()
        flash('Saved.', 'success')
        return redirect(url_for('blog.admin_categories'))
    cats = BlogCategory.query.order_by(BlogCategory.name.asc()).all()
    subs = BlogSubCategory.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    comments = BlogComment.query.order_by(BlogComment.created_at.desc()).all()
    return render_template('admin/blog_admin.html', categories=cats, subcategories=subs, posts=posts, comments=comments)


@blog_bp.route('/admin/categories/<int:cat_id>/delete', methods=['POST'])
def admin_delete_category(cat_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('blog.blog_list'))
    cat = BlogCategory.query.get(cat_id)
    if cat:
        # delete subcategories and related objects optionally
        db.session.delete(cat)
        db.session.commit()
    else:
        sub = BlogSubCategory.query.get_or_404(cat_id)
        db.session.delete(sub)
        db.session.commit()
    flash('Deleted.', 'success')
    return redirect(url_for('blog.admin_categories'))


@blog_bp.route('/admin/post/<int:post_id>/delete', methods=['POST'])
def admin_delete_post(post_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('blog.blog_list'))
    p = Post.query.get_or_404(post_id)
    # delete media files
    media_items = BlogMedia.query.filter_by(post_id=p.id).all()
    for m in media_items:
        try:
            path = os.path.join(current_app.root_path, 'static', m.file_path)
            if os.path.exists(path):
                os.remove(path)
        except Exception:
            pass
        db.session.delete(m)
    # delete comments
    BlogComment.query.filter_by(post_id=p.id).delete()
    db.session.delete(p)
    db.session.commit()
    flash('Post removed.', 'success')
    return redirect(url_for('blog.admin_categories'))


@blog_bp.route('/admin/comment/<int:comment_id>/delete', methods=['POST'])
def admin_delete_comment(comment_id):
    if session.get('user_role') != 'admin':
        flash('Access denied.', 'danger')
        return redirect(url_for('blog.blog_list'))
    c = BlogComment.query.get_or_404(comment_id)
    post_id = c.post_id
    db.session.delete(c)
    db.session.commit()
    flash('Comment removed.', 'success')
    return redirect(url_for('blog.admin_categories'))


# Like endpoint (API)
@blog_bp.route('/like/<int:post_id>', methods=['POST'])
def like_post(post_id):
    """Toggle like on a post. Returns JSON with like count."""
    post = Post.query.get_or_404(post_id)
    user_id = session.get('user_id')
    if not user_id:
        return {'success': False, 'msg': 'Login required'}, 401
    
    # Check if user already liked
    existing = Like.query.filter_by(post_id=post.id, user_id=user_id, comment_id=None).first()
    if existing:
        db.session.delete(existing)
        db.session.commit()
        # Reload the post to get updated like count
        post = Post.query.get(post_id)
        like_count = len(post.likes) if post.likes else 0
        return {'success': True, 'action': 'unliked', 'count': like_count}, 200
    else:
        like = Like(post_id=post.id, user_id=user_id)
        db.session.add(like)
        db.session.commit()
        # Reload the post to get updated like count
        post = Post.query.get(post_id)
        like_count = len(post.likes) if post.likes else 0
        return {'success': True, 'action': 'liked', 'count': like_count}, 200


# Reply to comment endpoint
@blog_bp.route('/comment/<int:comment_id>/reply', methods=['POST'])
def reply_comment(comment_id):
    """Add a reply to a comment."""
    comment = BlogComment.query.get_or_404(comment_id)
    body = request.form.get('body', '').strip()
    if not body:
        flash('Reply cannot be empty.', 'warning')
        return redirect(url_for('blog.blog_post', post_id=comment.post_id))
    
    author_id = session.get('user_id')
    author_name = session.get('user_name') or (User.query.get(author_id).name if author_id else 'Anonymous')
    reply = CommentReply(comment_id=comment.id, author_id=author_id, author_name=author_name, body=body)
    db.session.add(reply)
    db.session.commit()
    flash('Reply added.', 'success')
    return redirect(url_for('blog.blog_post', post_id=comment.post_id))
"""
Blog feature placeholder module.

This project is currently removing the blog feature for a redesign.
The original route handlers, models and templates were disabled/removed.
Keeping this placeholder file prevents accidental import errors while you
redesign the blog subsystem. You can delete this file later if desired.
"""

# No operational blueprint or route handlers here.
