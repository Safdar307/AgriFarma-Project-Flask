from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from flask_login import login_required
from db import db
from models.user import User
from forms.register_form import RegisterForm
from forms.login_form import LoginForm
import hashlib
import os
import uuid
from werkzeug.utils import secure_filename

auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth', static_folder='../static')

@auth_bp.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed = hashlib.sha256(form.password.data.encode()).hexdigest()
        picture_path = None
        file = request.files.get('picture')
        if file and file.filename:
            filename = secure_filename(file.filename)
            ext = os.path.splitext(filename)[1].lower()
            if ext in ['.jpg','.jpeg','.png','.gif','.webp']:
                unique = f"{uuid.uuid4().hex}{ext}"
                save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique)
                file.save(save_path)
                picture_path = f"uploads/avatars/{unique}"

        user = User(name=form.name.data, email=form.email.data, mobile=form.mobile.data,
                    location=form.location.data, profession=form.profession.data,
                    expertise=form.expertise.data, password=hashed, role='user', picture=picture_path)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please login to continue.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)

@auth_bp.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == hashlib.sha256(form.password.data.encode()).hexdigest():
            # Store user info in session
            session.clear()  # Clear any existing session data first
            session['user_id'] = user.id
            session['user_name'] = user.name
            session['user_email'] = user.email
            session['user_role'] = user.role
            session['user_picture'] = user.picture  # Store profile picture path
            flash('Logged in successfully.', 'success')
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            else:
                return redirect(url_for('home'))
        flash('Invalid email or password.', 'error')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('home'))

