from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, Email

class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    mobile = StringField('Mobile')
    location = StringField('Location')
    profession = SelectField('Profession', choices=[('farmer','Farmer'),('academics','Academics'),('consultant','Consultant'),('other','Other')])
    expertise = SelectField('Expertise', choices=[('expert','Expert'),('intermediate','Intermediate'),('beginner','Beginner')])
    password = PasswordField('Password', validators=[DataRequired()])
    picture = FileField('Profile Picture')
    submit = SubmitField('Register')
