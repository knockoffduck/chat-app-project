import unittest, datetime
from website import create_app, db
from flask import current_app
from flask_login import current_user, login_user, logout_user, AnonymousUserMixin
from website.models import User, Chat
from config import TestingConfig

class UserModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client()
        db.create_all()

        # Create test user and save it to the db
        u1 = User(
            firstname='Bob',
            lastname='Test',
            email='test@email.net',
            dob=datetime.datetime(2020, 1, 2),
            country="Aus",
            gender="Other"
        )
        u1.set_password('password')
        db.session.add(u1)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
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
        THEN check the response is invalid when login password is incorrect
        """

        with self.client:
            # Log in the user
            response = self.client.post('/auth/login',
                                        data={'email': 'test@email.net', 'password': 'pass'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Login', response.data)
            self.assertIn(b'Email', response.data)
            self.assertIn(b'Password', response.data)

            self.assertFalse(current_user.is_authenticated)

    def test_invalid_email_login(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/login' page is posted to (POST)
        THEN check the response is invalid when login email is incorrect
        """

        with self.client:
            # Log in the user
            response = self.client.post('/auth/login',
                                        data={'email': 'apple@email.net', 'password': 'password'},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            self.assertIn(b'Login', response.data)
            self.assertIn(b'Email', response.data)
            self.assertIn(b'Password', response.data)

            self.assertFalse(current_user.is_authenticated)

    def valid_registration(self):
        """ 
        GIVEN a Flask application configured for testing
        WHEN the '/auth/signup' page is posted to (POST)
        THEN check the response is valid
        """

        with self.client:
            response = self.client.post('/auth/signup', data={'firstname': 'Kelly',
                                                              'lastname': 'Stone',
                                                              'email': 'first@mail.com', 
                                                              'dob': datetime.datetime(1960, 11, 11),
                                                              'password': 'Horses',
                                                              'password2': 'Horses',
                                                              'country': 'India',
                                                              'gender': 'Female'},
                                                              follow_redirects=True)
            self.assertEqual(response.status_code, 200)

            with self.app.test_request_context():
                user = User.query.filter_by(email='test@email.net').first()
                login_user(user) 
                self.assertTrue(current_user.is_authenticated)
                self.assertEqual(current_user.email, user.email)
            logout_user()

        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)  