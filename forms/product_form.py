from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SubmitField, SelectField, BooleanField
from wtforms.validators import DataRequired, Email, Optional

class ProductForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    specifications = TextAreaField('Specifications', validators=[Optional()])
    price = FloatField('Price', default=0.0)
    seller_email = StringField('Seller Email', validators=[Optional(), Email()])
    category = SelectField('Category', coerce=int, validators=[Optional()])
    subcategory = SelectField('Sub-category', coerce=int, validators=[Optional()])
    active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
