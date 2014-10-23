#coding: utf-8

from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required

from models import db
from security.model import User#, Role
from flask.ext import admin, login


#user_datastore = SQLAlchemyUserDatastore(db, User, Role)
# security = Security(datastore=user_datastore)

login_manager = login.LoginManager()

# Create user loader function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)