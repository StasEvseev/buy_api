#coding: utf-8

from config import SECRET_KEY

from itsdangerous import JSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature

from models import db
from werkzeug.security import check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    login = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120))
    password = db.Column(db.String)

    # Flask-Login integration
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        s = Serializer(SECRET_KEY)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

    # Required for administrative interface
    def __unicode__(self):
        return self.username