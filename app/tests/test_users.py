import os
import unittest
from app import app, db

TEST_DB='user.db'

class UsersTests(unittest.TestCase):
    
    # setup and teardown
    
    # executed before each test
    
    def setUp(self):
        app.config['TESTING']=True
        app.config['WTF_CSRF_ENABLED']=False
        app.config['DEBUG']=False
        app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///' + os.path.join(app.config['BASEDIR'], TEST_DB)
        self.app=app.test_client()
        db.drop_all()
        db.create_all()
        
        self.assertEquals(app.debug, False)
    
    # executed after each test
    def tearDown(self):
        pass

    # helper methods
    def register(self, email, password, confirm):
        return self.app.post(
            '/register',
            data=dict(email=email, password=password, confirm=confirm),
            follow_redirects=True
        )        
    
    # tests
           
    def test_user_registration_form_displays(self):
        response=self.app.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please Register Your New Account', response.data)
    
    def test_valid_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        response=self.register('marundu@gmail.com', 'password123', 'password123')
        self.assertIn(b'Thank you for registering!', response.data)
    
    def test_duplicate_email_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        self.register('marundu@gmail.com', 'password123', 'password123')
        self.app.get('/register', follow_redirects=True)
        response=self.register('marundu@gmail.com', 'password123', 'password123')
        self.assertIn(b'ERROR! Email (marundu@gmail.com) already exists.', response.data)
    
    def test_missing_field_user_registration_error(self):
        self.app.get('/register', follow_redirects=True)
        response=self.register('marundu@gmail.com', 'password123', '')
        self.assertIn(b'This field is required.', response.data)

    def login(self, email, password):
        return self.app.post(
            '/login',
            data=dict(email=email, password=password),
            follow_redirects=True
            )

    def test_login_form_displays(self):
        response=self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)

    def test_valid_login(self):
        self.app.get('/register', follow_redirects=True)
        self.register('marundu@gmail.com', 'password123', 'password123')
        self.app.get('/login', follow_redirects=True)
        response=self.login('marundu@gmail.com', 'password123')
        self.assertIn(b'Thank you for logging in, marundu@gmail.com!', response.data)

    def test_login_without_registering(self):
        self.app.get('/login', follow_redirects=True)
        response=self.login('marundu@gmail.com', 'password123')
        self.assertIn(b'Incorrect log-in credentials!', response.data)

    def test_valid_logout(self):
        self.app.get('/register', follow_redirects=True)
        self.register('marundu@gmail.com', 'password123', 'password123')
        self.app.get('/login', follow_redirects=True)
        self.login('marundu@gmail.com', 'password123')
        response=self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Goodbye!', response.data)

    def test_invalid_logout_within_being_logged_in(self):
        response=self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Log In', response.data)

if __name__=='__main__':
    unittest.main()
