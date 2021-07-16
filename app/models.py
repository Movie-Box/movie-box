from enum import unique
from app import db, login, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, current_user
from datetime import datetime
from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
import jwt
from time import time
# from itsdangerous import TimedJSONWebSignatureSerialize as Serializer

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean, nullable=True, default=False)
    email_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    saved = db.relationship('Bookmark', backref='user', lazy='select')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_password_reset_token(self, expires_in=300):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')
    
    def get_verify_email_token(self, expires_in=300):
        return jwt.encode({'confirm_email': self.id, 'exp': time() + expires_in}, app.config['SECRET_KEY'], algorithm='HS256')
    
    @staticmethod
    def verify_password_reset_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)
    
    def verify_email_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=[
                            'HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)

class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    user = db.relationship(User)
    
    
class Bookmark(db.Model):
    __tablename__ = 'bookmark'
    id = db.Column(db.Integer, primary_key=True)
    media_id = db.Column(db.String(10), unique=True)
    media_type = db.Column(db.String(10))
    title = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    
    
@login.user_loader
def load_user(id):
    return User.query.get(int(id))