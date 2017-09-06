import unittest
from app import app

class ProjectTests(unittest.TestCase):
    
    # setup and teardown
    
    # executed before each test
    def setUp(self):
        app.config['TESTING']=True
        app.config['DEBUG']=False
        self.app=app.test_client()
        
        self.assertEquals(app.debug, False)
    
    # executed after each test
    def tearDown(self):
        pass
    
    # tests
    
    def test_main_page(self):
        response=self.app.get('/', follow_redirects=True)
        self.assertIn(b'Welcome!', response.data)
        self.assertIn(b'Breakfast', response.data)
        self.assertIn(b'Lunch', response.data)
        self.assertIn(b'Supper', response.data)
        self.assertIn(b'Dessert', response.data)

if __name__=='__main__':
    unittest.main()
