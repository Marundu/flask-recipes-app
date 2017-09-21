import os
import unittest
from app import app, db

TEST_DB='test.db'

class AppTests(unittest.TestCase):
    
    # setup and teardown
    
    # executed before each test
    
    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF_CSRF_ENABLED']=False
        app.config['DEBUG']=False
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app=app.test_client()
        db.create_all()
        
        self.assertEquals(app.debug, False)
     
    # executed after each test
    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    # tests
    
    def test_main_page(self):
        response=self.app.get('/', follow_redirects=True)
        self.assertIn(b'Recipe App', response.data)
        self.assertIn(b'Register', response.data)
        self.assertIn(b'Log In', response.data)
            
    def test_main_page_query_results(self):
        response=self.app.get('/add', follow_redirects=True)
        self.assertIn(b'Add a New Recipe', response.data)
    
    def test_add_recipe(self):
        response=self.app.post(
            '/add',
            data=dict(recipe_title='Hamburgers',
                    recipe_description='Delicious hamburgers'),
            follow_redirects=True)
        self.assertIn(b'New Recipe, Hamburgers, added!', response.data)
    
    def test_add_invalid_recipe(self):
        response=self.app.post(
            '/add',
            data=dict(recipe_title='',
                    recipe_description='Delicious hamburgers'),
            follow_redirects=True)
        self.assertIn(b'ERROR! Recipe was not added!', response.data)
        self.assertIn(b'This field is required.', response.data)

if __name__=='__main__':
    unittest.main()
