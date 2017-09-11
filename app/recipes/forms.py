from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class AddRecipeForm(Form):
    recipe_title=StringField('Recipe Title', validators=[DataRequired()])
    recipe_description=StringField('Recipe Description', validators=[DataRequired()])
