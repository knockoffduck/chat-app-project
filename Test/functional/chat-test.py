import unittest
from datetime import datetime
from website import create_app, db
from website.models import Chat, User
# check userid, timestamp, body 
class ChatModelTestCase(unittest.TestCase):
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

    def test_chat_properties(self):

        user = User(username='testuser')
        with self.app.app_context():
            db.session.add(user)
            db.session.commit()

        body = 'Hello, how are you?'
        timestamp = datetime.utcnow()
        chat = Chat(body=body, timestamp=timestamp, user_id=user.id)

        with self.app.app_context():
            db.session.add(chat)
            db.session.commit()

 
            self.assertEqual(chat.body, body)
            self.assertEqual(chat.timestamp, timestamp)
            self.assertEqual(chat.user_id, user.id)

if __name__ == '__main__':
    unittest.main()
