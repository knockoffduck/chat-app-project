import unittest
from website import create_app, db
from website.models import User
from website.forms import RegistrationForm

class RegistrationTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_registration_success(self):

        response = self.client.post('/register', data={
            'firstname': 'John',
            'lastname': 'Doe',
            'email': 'test@example.com',
            'password': '123456',
            'password2': '123456',
            'dob': '1990-01-01',
            'country': 'USA',
            'gender': 'M'
        }, follow_redirects=True)


        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registration successful!', response.data)
        self.assertIn(b'Login', response.data)


        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.firstname, 'John')
            self.assertEqual(user.lastname, 'Doe')
            self.assertEqual(user.dob, '1990-01-01')
            self.assertEqual(user.country, 'USA')
            self.assertEqual(user.gender, 'M')

if __name__ == '__main__':
    unittest.main()
