from flask_wtf import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from app import images

class AddRecipeForm(Form):
    recipe_title=StringField('Recipe Title', validators=[DataRequired()])
    recipe_description=StringField('Recipe Description', validators=[DataRequired()])
    recipe_image=FileField('Recipe Image', validators=[FileRequired(), FileAllowed(images, 'Images only!')])

class EmailForm(Form):
    email=StringField('Email', validators=[DataRequired(), Email(), Length(min=8, max=40)])
