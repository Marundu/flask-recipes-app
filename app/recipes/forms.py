from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class AddRecipeForm(Form):
    recipe_title=StringField('Recipe Title', validators=[DataRequired()])
    recipe_description=StringField('Recipe Description', validators=[DataRequired()])
