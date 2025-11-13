from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from db import db
from models.message import Message
from models.user import User
from forms.contact_form import ContactForm
from utils import admin_required

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/submit-message', methods=['POST'])
def submit_message():
    """Handle contact form submission"""
    form = ContactForm()
    
    if form.validate_on_submit():
        try:
            # Create new message
            new_message = Message(
                name=form.name.data,
                email=form.email.data,
                message=form.message.data,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_message)
            db.session.commit()
            
            flash('Thank you! Your message has been sent successfully. We will get back to you soon.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Sorry, there was an error sending your message. Please try again.', 'danger')
            print(f"Error saving message: {e}")
    else:
        # If form validation fails, flash errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field.capitalize()}: {error}', 'warning')
    
    # Redirect back to home page
    return redirect(url_for('home') + '#contact-section')

@contact_bp.route('/admin/messages', methods=['GET'])
@admin_required
def admin_messages():
    """Admin page to view all messages"""
    # Get all messages, ordered by creation date (newest first)
    messages = Message.query.order_by(Message.created_at.desc()).all()
    
    return render_template('admin/messages.html', messages=messages)

@contact_bp.route('/admin/messages/<int:message_id>/mark-read', methods=['POST'])
@admin_required
def mark_message_read(message_id):
    """Mark a message as read"""
    message = Message.query.get_or_404(message_id)
    message.status = 'read'
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Message marked as read'})

@contact_bp.route('/admin/messages/<int:message_id>/delete', methods=['POST'])
@admin_required
def delete_message(message_id):
    """Delete a message"""
    message = Message.query.get_or_404(message_id)
    db.session.delete(message)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Message deleted successfully'})

@contact_bp.route('/admin/messages/<int:message_id>/details', methods=['GET'])
@admin_required
def get_message_details(message_id):
    """Get message details for viewing in modal"""
    message = Message.query.get_or_404(message_id)
    
    return jsonify({
        'success': True,
        'message': {
            'id': message.id,
            'name': message.name,
            'email': message.email,
            'message': message.message,
            'status': message.status,
            'created_at': message.created_at.isoformat() if message.created_at else None
        }
    })