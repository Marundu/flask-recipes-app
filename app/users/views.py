from flask import Blueprint
from flask import render_template

# config

users_blueprint=Blueprint('users', __name__, template_folder='templates')

# routes

@users_blueprint.route('/login')
def login():
    return render_template('login.html')
