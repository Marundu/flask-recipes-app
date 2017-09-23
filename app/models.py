from app import bcrypt, db
from sqlalchemy.ext.hybrid import hybrid_method, hybrid_property

class Recipe(db.Model):
    
    __tablename__='recipes'
    
    id=db.Column(db.Integer, primary_key=True)
    recipe_title=db.Column(db.String, nullable=False)
    recipe_description=db.Column(db.String, nullable=False)
    
    def __init__(self, title, description):
        self.recipe_title=title
        self.recipe_description=description
    
    def __repr__(self):
        return '<Title {}>'.format(self.title)
    
class User(db.Model):

    __tablename__='users'
    
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String, unique=True, nullable=False)
    _password=db.Column(db.Binary(60), nullable=False)
    authenticated=db.Column(db.Boolean, default=False)
    
    def __init__(self, email, plaintext_password): 
        self.email=email
        self.password=plaintext_password
        self.authenticated=False

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def set_password(self, plaintext_password):
        self._password=bcrypt.generate_password_hash(plaintext_password)

    @hybrid_method
    def is_correct_password(self, plaintext_password):
        '''Return True if user is authenticated'''
        return bcrypt.check_password_hash(self.password, plaintext_password)
    
    @property
    def is_authenticated(self):
        '''Return True is user is authenticated'''
        return self.authenticated

    @property
    def is_active(self):
        '''Always True. All users are active'''
        return True

    @property
    def is_anonymous(self):
        '''Always False. Anonymouse users are not supported'''
        return False

    def get_id(self):
        '''Return the email address to satisfy Flask-Login requirements'''
        '''Requirs use of Python 3'''
        return str(self.id)
    
    def __repr__(self): 
        return '<User {}>'.format(self.name)
