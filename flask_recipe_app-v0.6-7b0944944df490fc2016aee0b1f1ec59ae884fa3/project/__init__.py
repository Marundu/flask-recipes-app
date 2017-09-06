#################
#### imports ####
#################

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


################
#### config ####
################

app = Flask(__name__, instance_relative_config=True)
app.config.from_pyfile('flask.cfg')

db = SQLAlchemy(app)


####################
#### blueprints ####
####################

from project.users.views import users_blueprint
from project.recipes.views import recipes_blueprint

# register the blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(recipes_blueprint)

