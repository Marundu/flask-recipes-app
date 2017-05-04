from flask import Flask

# config

app=Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

# blueprints

from app.users.views import users_blueprint
from app.recipes.views import recipes_blueprint

# register the blueprints

app.register_blueprint(users_blueprint)
app.register_blueprint(recipes_blueprint)
