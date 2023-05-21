import unittest, datetime, warnings
from website import create_app, db
from flask import current_app
from flask_login import current_user, login_user, logout_user, AnonymousUserMixin
from website.models import User, Chat
from config import TestingConfig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create test user and save it to the db
        u1 = User(
            firstname='Bob',
            lastname='Test',
            dob=datetime.datetime(2020, 1, 2),
            country="Aus",
            gender="Other"
        )
        u1.set_password('password')
        u1.set_email('test@email.net')
        db.session.add(u1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_password_hashing(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the a password is set and hashed
        THEN check that the password is hashed correctly
        """
        u = User(email='test@test.com')
        u.set_password('pass')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('pass'))
        


    def test_valid_login(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/login' page is posted to (POST)
        THEN check the response is valid
        """
        with self.client:
            # Log in the user
            response = self.client.post('/auth/login',
                                        data={'email': 'test@email.net', 'password': 'password'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            with self.app.test_request_context():
                user = User.query.filter_by(email='test@email.net').first()
                login_user(user) 
                self.assertTrue(current_user.is_authenticated)
                self.assertEqual(current_user.email, user.email)
            logout_user()
        self.assertEqual(response.status_code, 200)
        #check the chat screen comes up, where messages are sent
        self.assertIn(b'Send', response.data)

    #with help from ChatGPT
    def test_anonymous_user(self):
        """
        GIVEN a Flask application configured for testing
        WHEN no user is logged in
        THEN check if the current_user is an AnonymousUserMixin instance
        """

        with self.app.test_request_context():
            self.assertEqual(isinstance(current_user._get_current_object(), AnonymousUserMixin), True)


    def test_invalid_password_login(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/login' page is posted to (POST)
        THEN check the response is valid when login password is incorrect and shows correct page
        """

        with self.client:
            # Log in the user with incorrect password
            response = self.client.post('/auth/login',
                                        data={'email': 'test@email.net', 'password': 'pass'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            #make sure it redirects the login page again
            self.assertIn(b'Login', response.data)
            self.assertIn(b'Email', response.data)
            self.assertIn(b'Password', response.data)

            self.assertFalse(current_user.is_authenticated)


    def test_invalid_email_login(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/login' page is posted to (POST)
        THEN check the response is valid when login email is incorrect and shows correct page
        """

        with self.client:
            # Log in the user with incorrect email
            response = self.client.post('/auth/login',
                                        data={'email': 'apple@email.net', 'password': 'password'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Login', response.data)
            self.assertIn(b'Email', response.data)
            self.assertIn(b'Password', response.data)

            self.assertFalse(current_user.is_authenticated)


    def test_duplicate_registration(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/signup' page is posted to (POST) with email already registered
        THEN check the response is valid and throws an error message
        """
        with self.client:
            response = self.client.post('/auth/signup', data={'firstname': 'Bob',
                                                              'lastname': 'Test',
                                                              'email': 'test@email.net', 
                                                              'dob': datetime.datetime(2020, 1, 2),
                                                              'password': 'password',
                                                              'password2': 'password',
                                                              'country': 'Aus',
                                                              'gender': 'Other'},
                                                              follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Email address already registered', response.data)
            self.assertIn(b'Create Account', response.data)
            self.assertIn(b'Password', response.data)

            # check user is actually already in the db
            user = User.query.filter_by(email='test@email.net').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.firstname, 'Bob')
            self.assertEqual(user.lastname, 'Test')
            self.assertEqual(user.country, 'Aus')


    def test_valid_registration(self):
            """ 
            GIVEN a Flask application configured for testing
            WHEN the '/auth/signup' page is posted to (POST)
            THEN check the response is valid and completes registration
            """

            with self.client:
                response = self.client.post('/auth/signup', data={'firstname': 'Kelly',
                                                                  'lastname': 'Stone',
                                                                  'email': 'first@mail.com', 
                                                                  'dob': '1960-11-11',
                                                                  'password': 'Horse',
                                                                  'password2': 'Horse',
                                                                  'country': 'India',
                                                                  'gender': 'F'},
                                                                  follow_redirects=True)
                
                self.assertEqual(response.status_code, 200)

                #redirects to login page visually
                self.assertIn(b'Login', response.data)
                self.assertIn(b'Congratulations, you are now a registered user!', response.data)
                assert response.request.path == '/auth/login'
                
                # check user is added to the db
                user = User.query.filter_by(email='first@mail.com').first()
                self.assertIsNotNone(user)
                self.assertEqual(user.firstname, 'Kelly')
                self.assertEqual(user.lastname, 'Stone')
                self.assertEqual(user.country, 'India')

                #login
                response = self.client.post('/auth/login', data={'email': 'first@mail.com', 
                                                    'password': 'Horse'},
                                                    follow_redirects=True)
                self.assertEqual(response.status_code, 200)
                #prompted to chat
                assert response.request.path == '/chat'
                self.assertIn(b'Send', response.data)

    def test_invalid_email_registration(self):
            """ 
            GIVEN a Flask application configured for testing
            WHEN the '/auth/signup' page is posted to (POST) with incorrect email format
            THEN check the response is valid and returns warning
            """

            with self.client:
                response = self.client.post('/auth/signup', data={'firstname': 'Kelly',
                                                                  'lastname': 'Stone',
                                                                  'email': 'first', 
                                                                  'dob': '1960-11-11',
                                                                  'password': 'Horse',
                                                                  'password2': 'Horse',
                                                                  'country': 'India',
                                                                  'gender': 'F'},
                                                                  follow_redirects=True)
                
                self.assertEqual(response.status_code, 200)

                #returns correct error message
                self.assertIn(b'Create Account', response.data)
                self.assertIn(b'Invalid email address', response.data)
                assert response.request.path == '/auth/signup'

    def test_password_mismatch_registration(self):
            """ 
            GIVEN a Flask application configured for testing
            WHEN the '/auth/signup' page is posted to (POST) with mismatched passwords
            THEN check the response is valid and returns warning
            """

            with self.client:
                response = self.client.post('/auth/signup', data={'firstname': 'Kelly',
                                                                  'lastname': 'Stone',
                                                                  'email': 'first', 
                                                                  'dob': '1960-11-11',
                                                                  'password': 'Horse',
                                                                  'password2': 'Dog',
                                                                  'country': 'India',
                                                                  'gender': 'F'},
                                                                  follow_redirects=True)
                
                self.assertEqual(response.status_code, 200)

                #returns correct error message
                self.assertIn(b'Create Account', response.data)
                self.assertIn(b'Field must be equal to password', response.data)
                assert response.request.path == '/auth/signup'

    def test_successful_profile_update(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/account' page is posted (POST) with profile changed
        THEN check the response is valid and changes are saved
        """
        # Simulate the login process
        with self.client:
            response = self.client.post('/auth/login', data={'email': 'test@email.net', 
                                                             'password': 'password'}, 
                                                             follow_redirects = True)
            self.assertEqual(response.status_code, 200)

            # With successful login, access the account route
            self.assertEqual(current_user.email, 'test@email.net')
            response = self.client.get('/account',follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            #change first name
            response = self.client.post('/account', data={'firstname': 'Jane',
                                                           'lastname': 'Smith',
                                                           'dob': '1995-02-15',
                                                           'country': 'Canada',
                                                           'gender': 'F'}, 
                                                            follow_redirects=True)
            assert response.request.path == '/account'
            self.assertIn(b'Success! Your changes have been saved', response.data)
                            
            # check user is updated to the db
            user = User.query.filter_by(email='test@email.net').first()
            self.assertEqual(user.firstname, 'Jane')
            self.assertEqual(user.lastname, 'Smith')
            self.assertEqual(user.dob.strftime('%Y-%m-%d'), '1995-02-15')
            self.assertEqual(user.country, 'Canada')
            self.assertEqual(user.gender, 'F')
                          

if __name__ == '__main__':
    unittest.main(verbosity=2)