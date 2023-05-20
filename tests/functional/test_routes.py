import unittest, datetime, warnings
from website import create_app, db
from website.models import User, Chat
from config import Config, TestingConfig
from flask_login import current_user

class RouteTestCase(unittest.TestCase):
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


    def test_home_route(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
        """
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'The support you need,' in response.data
        assert b'Deep learning' in response.data

    def test_login_route(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/login' page is requested (GET)
        THEN check the response is valid
        """
        response = self.client.get('/auth/login')
        assert response.status_code == 200
        assert b'Login' in response.data
        assert b'New User?' in response.data

    def test_signup_route(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/signup' page is requested (GET)
        THEN check the response is valid
        """
        response = self.client.get('/auth/signup')
        assert response.status_code == 200
        assert b'Create Account' in response.data
        assert b'To access the benefits of MindMate' in response.data
        assert b'Email' in response.data
        assert b'Country' in response.data


    def test_chat_route(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/chat' page is requested (GET)
        THEN check the response is valid
        """
        # Simulate the login process
        with self.client:
            response = self.client.post('/auth/login', data={'email': 'test@email.net', 
                                                             'password': 'password'}, 
                                                             follow_redirects = True)
            self.assertEqual(response.status_code, 200)

            # With successful login, access the chat route
            self.assertEqual(current_user.email, 'test@email.net')
            response = self.client.get('/chat',follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            assert response.request.path == '/chat'
            assert b'Chat' in response.data
            assert b'Send a message' in response.data

    def test_account_route(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/account' page is requested (GET)
        THEN check the response is valid
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

            #check that account details are on account page
            assert response.request.path == '/account'
            assert b'Account' in response.data
            assert b'First Name' in response.data
            assert b'Last Name' in response.data
            assert b'Date Of Birth' in response.data
            assert b'Country' in response.data
            assert b'Gender' in response.data
            self.assertIn(current_user.firstname, response.data.decode('utf-8'))
            self.assertIn(current_user.lastname, response.data.decode('utf-8'))
            self.assertIn(current_user.country, response.data.decode('utf-8'))
            self.assertIn(current_user.gender, response.data.decode('utf-8'))


    # def test_history_route(self):
    #     """ 
    #     GIVEN a Flask application configured for testing
    #     WHEN the '/history/1' page is requested (GET)
    #     THEN check the response is valid
    #     """
    #     # Simulate the login process
    #     with self.client:
    #         response = self.client.post('/auth/login', data={'email': 'test@email.net', 
    #                                                          'password': 'password'}, 
    #                                                          follow_redirects = True)
    #         self.assertEqual(response.status_code, 200)

    #         # With successful login, access the history route
    #         self.assertEqual(current_user.email, 'test@email.net')
    #         response = self.client.get('/history/1',follow_redirects=True)
    #         self.assertEqual(response.status_code, 200)

    #         #check that account details are on account page
    #         assert response.request.path == '/history/1'


if __name__ == '__main__':
    unittest.main(verbosity=2)
