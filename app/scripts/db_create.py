from app import db
from app.models import Recipe

# create the database and the database tables
db.create_all()

# insert recipe data
recipe1=Recipe('Omena', 'Omena cooked with onion and pepper. Perfect with ugali.')
recipe2=Recipe('Scrambled Eggs', 'Eggs fried with onions, tomatoes, dhania, and green peppers.')
recipe3=Recipe('Chicken Biriani', 'Stewed chicken in spices.')

db.session.add([recipe1, recipe2, recipe3])

# commit the changes
db.session.commit()
