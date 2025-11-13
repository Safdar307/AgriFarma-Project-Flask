from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError
from flask_wtf.file import FileAllowed
from models.consultant import Consultant
from db import db

class ConsultantApplicationForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(min=10, max=20)])
    expertise_category = SelectField('Area of Expertise', coerce=int, validators=[DataRequired()])
    bio = TextAreaField('Bio/Experience Description', validators=[DataRequired(), Length(min=100, max=2000)])
    profile_picture = FileField('Profile Picture', validators=[
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])
    submit = SubmitField('Submit Application')
    
    def validate_email(self, field):
        """Custom validator to check for duplicate email addresses"""
        email = field.data.strip().lower()
        
        # Check if email already exists in consultant table
        existing_consultant = Consultant.query.filter(
            db.func.lower(Consultant.email) == email
        ).first()
        
        if existing_consultant:
            raise ValidationError('This email address is already associated with a consultant application. If you need to update your information, please contact the administrator.')