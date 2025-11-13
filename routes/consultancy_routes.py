from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from utils import admin_required
from models.category import Category
from models.consultant import Consultant
from forms.consultancy_forms import ConsultantApplicationForm
from werkzeug.utils import secure_filename
import os
from db import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError

consultancy_bp = Blueprint('consultancy', __name__)

# User-facing routes
@consultancy_bp.route('/consultant/apply', methods=['GET', 'POST'])
def apply_consultant():
    form = ConsultantApplicationForm()
    
    # Populate category choices
    categories = Category.query.all()
    form.expertise_category.choices = [(0, 'Select a category')] + [(c.id, c.name) for c in categories]
    
    if form.validate_on_submit():
        try:
            # Handle profile picture upload
            profile_picture_path = None
            if form.profile_picture.data:
                filename = secure_filename(form.profile_picture.data.filename)
                # Save to uploads/consultants directory
                filepath = os.path.join('static', 'uploads', 'consultants', filename)
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                form.profile_picture.data.save(filepath)
                # Store relative path from static directory
                profile_picture_path = os.path.join('uploads', 'consultants', filename)

            new_consultant = Consultant(
                name=form.name.data,
                email=form.email.data.lower().strip(),  # Normalize email
                phone=form.phone.data,
                expertise_category=form.expertise_category.data,
                bio=form.bio.data,
                profile_picture=profile_picture_path
            )
            
            db.session.add(new_consultant)
            db.session.commit()
            
            flash('Your application has been submitted successfully! It is now pending admin approval.', 'success')
            return redirect(url_for('consultancy.apply_consultant'))
            
        except IntegrityError as e:
            # Handle any remaining database integrity issues
            db.session.rollback()
            if 'UNIQUE constraint failed' in str(e) and 'consultant.email' in str(e):
                flash('An application with this email address already exists. Please use a different email address.', 'danger')
            elif 'NOT NULL constraint failed' in str(e):
                flash('Please fill in all required fields.', 'danger')
            else:
                flash('There was an error submitting your application. Please try again.', 'danger')
            
        except Exception as e:
            # Handle any other unexpected errors
            db.session.rollback()
            print(f"Unexpected error in apply_consultant: {e}")
            flash('An unexpected error occurred. Please try again later.', 'danger')
    
    return render_template('consultant/apply.html', form=form)

@consultancy_bp.route('/browse')
def browse_consultants():
    categories = Category.query.all()
    consultants = Consultant.query.filter_by(status='approved').all()
    return render_template('consultant/browse.html', 
                         categories=categories,
                         consultants=consultants)

# Admin routes
@consultancy_bp.route('/admin/consultancy')
@admin_required
def admin_consultancy():
    # Get pending consultants
    pending_consultants = Consultant.query.filter_by(status='pending').all()
    approved_consultants = Consultant.query.filter_by(status='approved').all()
    categories = Category.query.all()
    
    return render_template('admin/consultancy/dashboard.html',
                         categories=categories,
                         pending_consultants=pending_consultants,
                         approved_consultants=approved_consultants)

@consultancy_bp.route('/admin/consultant/<int:id>/<string:action>', methods=['POST'])
@admin_required
def handle_consultant_application(id, action):
    consultant = Consultant.query.get_or_404(id)
    if action == 'approve':
        consultant.status = 'approved'
        flash('Consultant application approved!', 'success')
    elif action == 'reject':
        consultant.status = 'rejected'
        flash('Consultant application rejected!', 'success')
    
    consultant.updated_at = datetime.utcnow()
    db.session.commit()
    return redirect(url_for('consultancy.admin_consultancy'))

@consultancy_bp.route('/admin/consultant/<int:id>/delete', methods=['POST'])
@admin_required
def delete_consultant(id):
    consultant = Consultant.query.get_or_404(id)
    
    # Store consultant name for flash message
    consultant_name = consultant.name
    
    # Delete associated profile picture file if it exists
    if consultant.profile_picture:
        try:
            profile_path = os.path.join('static', consultant.profile_picture)
            if os.path.exists(profile_path):
                os.remove(profile_path)
        except Exception as e:
            print(f"Warning: Could not delete profile picture: {e}")
    
    # Delete the consultant from database
    db.session.delete(consultant)
    db.session.commit()
    
    flash(f'Consultant "{consultant_name}" has been deleted successfully!', 'success')
    return redirect(url_for('consultancy.admin_consultancy'))