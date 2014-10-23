#coding: utf-8


from flask import Flask, redirect
from flask.ext.triangle import Triangle



from config import DATABASE_URI, SECRET_KEY


def create_app():
    from resources import api
    from models import db
    from admin import admin
    from assets import assets
    from security import login_manager

    application = Flask(__name__)
    application.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    application.config['SECRET_KEY'] = SECRET_KEY

    Triangle(application)
    assets.init_app(application)
    api.init_app(application)
    db.init_app(application)
    admin.init_app(application)
    login_manager.init_app(application)

    return application

app = create_app()

@app.route('/')
def index():
    return redirect("/admin")

if __name__ == "__main__":
    app.run(debug=True)