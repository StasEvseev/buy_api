#coding: utf-8
from flask import make_response, jsonify, g

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from models import db
from security.model import User#, Role
from flask.ext import admin, login
from flask.ext.httpauth import HTTPBasicAuth


#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(datastore=user_datastore)

login_manager = login.LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)

auth = HTTPBasicAuth()

# @auth.get_password
# def get_password(username):
#     if username == 'miguel':
#         return 'python'
#     return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(login = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    #g.user = user
    return True