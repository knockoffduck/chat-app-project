import unittest, datetime
from website import create_app, db
from website.models import User, Chat
from config import TestingConfig

class UserModelCase(unittest.TestCase):
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

    def test_password_hashing(self):
        u = User(email='test@test.com')
        u.set_password('pass')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('pass'))

    # def test_login_with_invalid_details(self):
    #     u = User(email='test@test.com')
    #     u.set_password('pass')

    # def test_register(self):


if __name__ == '__main__':
    unittest.main(verbosity=2)