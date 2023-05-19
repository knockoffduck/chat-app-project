import unittest, datetime
from website import create_app, db
from website.models import User, Chat
from config import Config, TestingConfig

class RouteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        u1 = User(firstname='Bob',lastname='Test',email='test@email.net',dob=datetime.datetime(2020,1,2),country="Aus",gender="Other")
        u1.set_password('password')
        db.session.add(u1)
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

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
        assert b'To access the benefits of' in response.data
        assert b'Country' in response.data

    def test_chat_route(self):
        # Simulate the login process
        with self.client:
            response = self.client.post('/auth/login', data={'email': 'test@email.net', 'password': 'password'})
            self.assertEqual(response.status_code, 200)

            # Assuming the login is successful, you can access the chat route
            response = self.client.get('/chat')
            self.assertEqual(response.status_code, 200)

        assert b'Chat' in response.data
        assert b'Send a message.' in response.data



if __name__ == '__main__':
    unittest.main(verbosity=2)
