import unittest
from website import create_app, db
from website.models import User
from website.forms import EditProfileForm

class EditProfileTestCase(unittest.TestCase):
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

    def test_edit_profile(self):

        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password',
            'remember_me': False
        })
        # check link
        response = self.client.get('/profile/edit')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/profile/edit', data={
            'firstname': 'Jane',
            'lastname': 'Smith',
            'dob': '1995-02-15',
            'country': 'Canada',
            'gender': 'F'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Profile updated successfully', response.data)

        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertEqual(user.firstname, 'Jane')
            self.assertEqual(user.lastname, 'Smith')
            self.assertEqual(user.dob.strftime('%Y-%m-%d'), '1995-02-15')
            self.assertEqual(user.country, 'Canada')
            self.assertEqual(user.gender, 'F')

    def test_upload_avatar(self):
        #  avatar
        avatar_path = '/path/to/avatar.png'  

        # login
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password',
            'remember_me': False
        })

        # upload avatar
        with open(avatar_path, 'rb') as avatar_file:
            response = self.client.post('C:\Desktop\Avatar.png', data={
                'user_avatar': (avatar_file, 'avatar.png')
            }, follow_redirects=True)

        # check avatar link
        with self.app.app_context():
            user = User.query.filter_by(email='test@example.com').first()
            self.assertEqual(user.avatar, 'C:\Desktop\Avatar.png')  
if __name__ == '__main__':
    unittest.main()
