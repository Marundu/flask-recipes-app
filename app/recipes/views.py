from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for

from forms import AddRecipeForm

from app import db
from app.models import Recipe

# config

recipes_blueprint=Blueprint('recipes', __name__, template_folder='templates')

# helper functions

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - %s' % (getattr(form, field).label.text,
            error
            ), 'info')

# routes

@recipes_blueprint.route('/')
def index():
    all_recipes=Recipe.query.all()
    return render_template('recipes.html', recipes=all_recipes)

@recipes_blueprint.route('/add', methods=['GET', 'POST'])
def add_recipe():
    form=AddRecipeForm(request.form)
    if request.method=='POST':
        if form.validate_on_submit():
            new_recipe=Recipe(form.recipe_title.data, form.recipe_description.data)
            db.session.add(new_recipe)    
            db.session.commit()
            flash('New Recipe, {}, added!'.format(new_recipe.recipe_title), 'success')
            return redirect(url_for('recipes.index'))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not added!', 'error')
    
    return render_template('add_recipe.html', form=form)
