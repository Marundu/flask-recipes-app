from app import db
from app.models import Recipe
from app.models import User

# drop existing database tables

print 'Dropping existing database tables...'
db.drop_all() 

# create the database and the database tables

print 'Creating database tables...'
db.create_all() 

# insert user data

admin_user=User(email='marundu@gmail.com', plaintext_password='adminpassword', role='admin')

user1=User(email='ruf@ruf.com', plaintext_password='password123', role='user')
user2=User(email='me@marundu.co.ke', plaintext_password='ovacodol', role='user')
user3=User(email='covfefe@cov.com', plaintext_password='password', role='user')
user4=User(email='madodo@gmail.com', plaintext_password='oldpassword', role='user')

# add users to db

print 'Inserting user data...'
db.session.add_all([admin_user, user1, user2, user3, user4])

# insert recipe data: title, description, is_public, user_id

recipe1=Recipe('Omena', 'Omena cooked with onion and pepper.', False, admin_user.id)
recipe2=Recipe('Scrambled Eggs', 'Eggs fried with onions, tomatoes, and green peppers.', True, admin_user.id)
recipe3=Recipe('Chicken Biriani', 'Stewed chicken in spices.', True, user1.id)
recipe4=Recipe('Kamande', 'Fried lentils in onions and spices', True, user3.id)

# add recipes to db

print 'Inserting recipe data...'
db.session.add_all([recipe1, recipe2, recipe3, recipe4])

# commit the changes
db.session.commit()

print 'Done!' 
