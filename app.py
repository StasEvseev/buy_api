#coding: utf-8
from datetime import timedelta

from flask import Flask, redirect, request
from flask.ext.triangle import Triangle
from flask.ext.babel import Babel

from werkzeug.contrib.fixers import ProxyFix

from resources import api
from models import db
from admin import admin
from assets import assets
from security import login_manager

from config import DATABASE_URI, SECRET_KEY
from log import init_logging


def create_app():
    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    # application.config['BABEL_DEFAULT_LOCALE'] = 'ru-ru'
    application.config['SECRET_KEY'] = SECRET_KEY
    application.permanent_session_lifetime = timedelta(minutes=30)

    Triangle(application)
    assets.init_app(application)
    api.init_app(application)
    api.application = application
    db.init_app(application)
    admin.init_app(application)
    login_manager.init_app(application)
    application.db = db
    application.api = api

    babel = Babel(application)
    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(["ru"])

    init_logging(application)

    return application

app = create_app()
app.wsgi_app = ProxyFix(app.wsgi_app)

@app.route('/')
def index():
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)