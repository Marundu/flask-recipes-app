from app import db

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
    password_plaintext=db.Column(db.String, nullable=False) # temporary. add hashing
    
    def __init__(self, email, password_plaintext): 
        self.email=email
        self.password_plaintext=password_plaintext
    
    def __repr__(self): 
        return '<User {}>'.format(self.name)
