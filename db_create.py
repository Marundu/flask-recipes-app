from app import db
from app.models import Recipe
from app.models import User

# drop existing database tables
db.drop_all() 

# create the database and the database tables
db.create_all() 

# insert recipe data
recipe1=Recipe('Omena', 'Omena cooked with onion and pepper.')
recipe2=Recipe('Scrambled Eggs', 'Eggs fried with onions, tomatoes, and green peppers.')
recipe3=Recipe('Chicken Biriani', 'Stewed chicken in spices.')
recipe4=Recipe('Kamande', 'Fried lentils in onions and spices')

# add recipes to db

db.session.add_all([recipe1, recipe2, recipe3, recipe4])

# insert user data

admin_user=User(email='marundu@gmail.com', plaintext_password='adminpassword', role='admin')

user1=User('ruf@ruf.com', 'password123')
user2=User('me@marundu.co.ke', 'ovacodol')
user3=User('covfefe@cov.com', 'password')
user4=User('madodo@gmail.com', 'oldpassword')

# add users to db

db.session.add_all([admin_user, user1, user2, user3, user4])

# commit the changes
db.session.commit()
