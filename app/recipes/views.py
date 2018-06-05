from flask import Blueprint
from flask import flash
from flask import render_template
from flask import redirect
from flask import request
from flask import url_for
from flask_login import current_user, login_required

from .forms import AddRecipeForm

from app import db
from app.models import Recipe

# config

recipes_blueprint=Blueprint('recipes', __name__)

# helper functions

def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u'Error in the %s field - %s' % (getattr(form, field).label.text,
            error
            ), 'info')

# routes

# display public recipes

@recipes_blueprint.route('/')
def public_recipes():
    all_public_recipes=Recipe.query.filter_by(is_public=True)
    return render_template('public_recipes.html', public_recipes=all_public_recipes)

# display user recipes 

@recipes_blueprint.route('/recipes')
@login_required
def user_recipes():
    all_user_recipes=Recipe.query.filter_by(user_id=current_user.id)
    return render_template('user_recipes.html', user_recipes=all_user_recipes)

# add a recipe

@recipes_blueprint.route('/add', methods=['GET', 'POST'])
@login_required
def add_recipe():
    form=AddRecipeForm(request.form)
    if request.method=='POST':
        if form.validate_on_submit():
            new_recipe=Recipe(form.recipe_title.data, form.recipe_description.data, False, current_user.id) # True
            db.session.add(new_recipe)    
            db.session.commit()
            flash('New Recipe, {}, added!'.format(new_recipe.recipe_title), 'success')
            return redirect(url_for('recipes.user_recipes'))
        else:
            flash_errors(form)
            flash('ERROR! Recipe was not added!', 'error')
    
    return render_template('add_recipe.html', form=form)

