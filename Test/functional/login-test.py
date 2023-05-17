import unittest
from website import create_app, db
from website.models import User
from website.forms import LoginForm

class LoginTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

            user = User(
                email='test@example.com',
                password='password',
                firstname='John',
                lastname='Doe',
                dob='1990-01-01',
                country='USA',
                gender='M'
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):

        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password',
            'remember_me': False
        }, follow_redirects=True)


        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome, John!', response.data)
        self.assertIn(b'Logout', response.data)

    def test_login_failure(self):

        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'wrong_password',
            'remember_me': False
        }, follow_redirects=True)


        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)
        self.assertIn(b'Login', response.data)

if __name__ == '__main__':
    unittest.main()
