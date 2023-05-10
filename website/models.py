from website import db
from .__init__ import login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
  
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(30))
    lastname = db.Column(db.String(40))
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    dob = db.Column(db.DateTime)
    country = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    chat = db.relationship('Chat', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.email)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Chat {}>'.format(self.body)
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))